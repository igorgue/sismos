"""
bot.py

This is the bot for the webhooks of Twilio's WhatsApp API.
"""
import os

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
    usage_message = "Comandos: [ultimos|ayuda]"
    message = message.lower()

    if message in ["ultimos", "últimos"]:
        response.message(_get_last_sismos(db))
    elif message == "ayuda":
        response.message(usage_message)
    else:
        print(f"Unknown command: {message}")

        response.message(usage_message)

    return response.to_xml()


def _get_last_sismos(db: Session) -> str:  # pylint: disable=invalid-name
    """
    Get the last sismos from the database.
    """
    assert db

    prefix = "Sismos: \n\n"

    content = ""
    for sismo in Sismo.latest(db):
        content += f"{sismo.richter} - {sismo.location} - {sismo.country} - {sismo.created}\n"

    sufix = "\n\nFuente: https://www.ineter.gob.ni/sismos/"

    return prefix + content + sufix
