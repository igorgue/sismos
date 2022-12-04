"""
bot.py

This is the bot for the webhooks of Twilio's WhatsApp API.
"""
import os

from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

# Your Account SID from twilio.com/console
account_sid = os.getenv("TWILIO_ACCOUNT_SID") or "YOUR_ACCOUNT_SID"
# Your Auth Token from twilio.com/console
auth_token = os.getenv("TWILIO_ACCOUNT_AUTH") or "YOUR_ACCOUNT_TOKEN"

client = Client(account_sid, auth_token)


def respond(message: str) -> str:
    """
    Respond to the message with the given content.
    """
    # TODO: Write actual rules to send messages.
    response = MessagingResponse()
    response.message(f"Echo: {message}")

    return response.to_xml()
