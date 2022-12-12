"""
bot.py

This is the bot for the webhooks of Twilio's WhatsApp API.
"""
import os
from datetime import datetime, timedelta
from functools import lru_cache
from string import Template
from typing import Optional

import openai
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from sismos.location import NICARAGUAN_STATES
from sismos.models import Sismo, exec_generic_statement

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY"

# Your Account SID from twilio.com/console
account_sid = os.getenv("TWILIO_ACCOUNT_SID") or "YOUR_ACCOUNT_SID"
# Your Auth Token from twilio.com/console
auth_token = os.getenv("TWILIO_ACCOUNT_AUTH") or "YOUR_ACCOUNT_TOKEN"

client = Client(account_sid, auth_token)


def respond(db: Session, message: str) -> str:  # pylint: disable=invalid-name
    """
    Respond to the message with the given content.
    """
    response = MessagingResponse()
    message = message.lower()

    if _is_ultimos(message):
        response.message(_get_last_sismos(db))
    elif _is_ayuda(message):
        response.message(_get_help())
    else:
        print(f"Unknown command: {message}")

        response.message(_get_help())

    return response.to_xml()


def respond_with_ai(db: Session, message: str) -> str:  # pylint: disable=invalid-name
    """
    Respond to the message with the given content.
    """
    response = MessagingResponse()
    message = message.lower()

    location_prompt = create_locations_ai_prompt(message)

    ai_locations_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=location_prompt,
        temperature=0.7,
        max_tokens=50,
    )

    if ai_locations_response["choices"][0]["text"] != "NO_LOCATION_PRESENT":  # type: ignore
        sismos_prompt = create_sismos_ai_prompt(message)
        ai_sismos_response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=sismos_prompt,
            temperature=0.7,
            max_tokens=150,
        )
    else:
        lat, long = NICARAGUAN_STATES[ai_locations_response["choices"][0]["text"]]  # type: ignore
        sismos_prompt = create_sismos_ai_prompt(message, lat, long)
        ai_sismos_response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=sismos_prompt,
            temperature=0.7,
            max_tokens=150,
        )

    sql_stmt: str = ai_sismos_response["choices"][0]["text"]  # type: ignore
    sql_stmt = sql_stmt.replace("\n", " ").strip()

    print(f"Sismos SQL: {sql_stmt}")

    if sql_stmt.lower().startswith('select * from "sismos"'):
        response.message(
            _format_from_results(Sismo.exec_select_statement(db, sql_stmt))
        )
    elif sql_stmt.lower().startswith("select count"):
        response.message(
            _format_from_simple_counts(exec_generic_statement(db, sql_stmt))
        )
    else:
        response.message(_get_help())

    return response.to_xml()


def create_sismos_ai_prompt(
    message: str, lat: Optional[float] = None, long: Optional[float] = None
) -> str:
    """
    Get the prompt from the user for the sismos.
    """
    assert message, "The message cannot be empty"

    if not lat or not long:
        return _get_template("query.sismos.ai.txt").safe_substitute(prompt=message)

    location_query = f"lat = {lat} and long = {long}"

    return _get_template("query.sismos.ai.txt").safe_substitute(
        prompt=message, extra_info=location_query
    )


def create_locations_ai_prompt(message: str) -> str:
    """
    Get the prompt from the user for location.
    """
    assert message, "The message cannot be empty"

    return _get_template("query.locations.ai.txt").safe_substitute(prompt=message)


@lru_cache
def _get_template(template_name: str) -> Template:
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_file_path, template_name)

    with open(filename, "r", encoding="utf-8") as file:
        template_content = file.read()

    assert template_content, "Template is empty"

    return Template(template_content)


def _is_ultimos(message: str) -> bool:
    """
    Check if the message is for the last sismos.
    """
    conds = (
        message in ["ultimos", "últimos"]
        or message.startswith("ult")
        or message.startswith("últ")
        or message.startswith("lastest")
        or message.startswith("last")
    )

    return conds


def _is_ayuda(message: str) -> bool:
    """
    Check if the message is for the help.
    """
    conds = (
        message in ["ayuda", "help"]
        or message.startswith("ayu")
        or message.startswith("hel")
    )

    return conds


def _get_last_sismos(db: Session) -> str:  # pylint: disable=invalid-name
    """
    Get the last sismos from the database.
    """
    assert db

    return _format_from_results(Sismo.get_last_sismos(db))


def _format_from_simple_counts(result: str) -> str:
    content = f"{result}"

    footer = "\n\nFuente: INETER (Nicaragua)"

    return content + footer


def _format_from_results(results: list[Sismo]) -> str:
    header = "Sismos: \n\n"

    content = ""
    for sismo in results:
        country_emoji = country_to_flag_emoji(str(sismo.country))
        country_abbr = country_to_abbr(str(sismo.country))
        richter_emoji = richter_scale_to_emoji(str(sismo.richter))
        time_ago = datetime_to_time_ago_in_spanish(sismo.created)  # type: ignore

        content += (
            f"{country_abbr} {country_emoji}: {sismo.richter} {richter_emoji}\n"
            f"{sismo.location}. {time_ago}\n\n"
        )

    # footer = (
    #     "\n\nFuente: "
    #     "https://ineter.gob.ni/articulos/areas-tecnicas/"
    #     "geofisica/monitoreo-de-sismos-en-tiempo-real.html"
    # )
    footer = "\n\nFuente: INETER (Nicaragua)"

    return header + content + footer


def _get_help() -> str:
    """
    Get the help message.
    """
    return (
        "Comandos: [ultimos|ayuda], escala:\n\n"
        "🌋: 0.0 - 2.9\n"
        "🌋🌋: 3.0 - 3.9\n"
        "🌋🌋🌋: 4.0 - 5.9\n"
        "🌋🌋🌋🌋: 6.0 - 6.9\n"
        "🌋🌋🌋🌋🌋: 7.0 - ..."
    )


def country_to_flag_emoji(country: str) -> str:
    """
    Convert the country to the flag emoji.
    """
    assert country

    data = {
        "Nicaragua": "🇳🇮",
        "Costa Rica": "🇨🇷",
        "Panama": "🇵🇦",
        "Panamá": "🇵🇦",
        "Honduras": "🇭🇳",
        "El Salvador": "🇸🇻",
        "Guatemala": "🇬🇹",
        "Mexico": "🇲🇽",
        "México": "🇲🇽",
    }

    return data.get(country, "")


def country_to_abbr(country: str) -> str:
    """
    Convert the country to the abbreviation.
    """
    assert country

    data = {
        "Nicaragua": "NI",
        "Costa Rica": "CR",
        "Panama": "PA",
        "Panamá": "PA",
        "Honduras": "HN",
        "El Salvador": "SV",
        "Guatemala": "GT",
        "Mexico": "MX",
        "México": "MX",
    }

    return data.get(country, "")


def richter_scale_to_emoji(richter: str) -> str:
    """
    Convert the richter scale to the emoji.
    """
    ritcher = float(richter)

    if ritcher <= 2.9:
        return "🌋"
    if ritcher <= 3.9:
        return "🌋🌋"
    if ritcher <= 5.9:
        return "🌋🌋🌋"
    if ritcher <= 6.9:
        return "🌋🌋🌋🌋"

    return "🌋🌋🌋🌋🌋"


def datetime_to_time_ago_in_spanish(  # pylint: disable=too-many-return-statements
    date: datetime,
) -> str:
    """
    Convert the datetime to the time ago in spanish.
    """
    assert date

    # datetime.now() with timezone from Nicaragua
    now = datetime.now() - timedelta(hours=-6)
    diff = now - date

    if diff.days > 0:
        if diff.days == 1:
            return "hace 1 día"

        return f"hace {diff.days} días"

    hours = diff.seconds // 3600
    if hours > 0:
        if hours == 1:
            return "hace 1 hora"

        return f"hace {hours} horas"

    minutes = diff.seconds // 60
    if minutes > 0:
        if minutes == 1:
            return "hace 1 minuto"

        return f"hace {minutes} minutos"

    return "hace unos segundos"
