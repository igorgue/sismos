"""
bot.py

This is the bot for the webhooks of Twilio's WhatsApp API.
"""
import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from sismos.models import Sismo

load_dotenv()

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

    prefix = "Sismos: \n\n"

    content = ""
    for sismo in Sismo.latest(db):
        country_emoji = country_to_flag_emoji(str(sismo.country))
        country_abbr = country_to_abbr(str(sismo.country))
        richter_emoji = richter_scale_to_emoji(str(sismo.richter))
        time_ago = datetime_to_time_ago_in_spanish(sismo.created)  # type: ignore

        content += (
            f"{country_abbr} {country_emoji}: {sismo.richter} {richter_emoji}\n"
            f"{sismo.location}. {time_ago}\n\n"
        )

    sufix = (
        "\n\nFuente: "
        "https://ineter.gob.ni/articulos/areas-tecnicas/"
        "geofisica/monitoreo-de-sismos-en-tiempo-real.html"
    )

    return prefix + content + sufix


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
        "Honduras": "🇭🇳",
        "El Salvador": "🇸🇻",
        "Guatemala": "🇬🇹",
        "Mexico": "🇲🇽",
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
        "Honduras": "HN",
        "El Salvador": "SV",
        "Guatemala": "GT",
        "Mexico": "MX",
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

    now = datetime.now()
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
