"""
api.py

This is the api for the webhooks of Twilio's WhatsApp API.
"""
from logging import getLogger

from fastapi import FastAPI, Request

log = getLogger(__name__)

app = FastAPI()

@app.post("/whatsapp/incoming")
def whatsapp_incoming(_: Request):
    """
    This is the webhook for incoming messages.
    """
    data = {"message": "Sismos API (reply)"}

    log.info(data)

    return data

@app.post("/whatsapp/status")
def whatsapp_status(_: Request):
    """
    This is the webhook for status updates.
    """
    data = {"message": "Sismos API (status)"}

    log.info(data)

    return data
