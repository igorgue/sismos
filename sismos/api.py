"""
api.py

This is the api for the webhooks of Twilio's WhatsApp API.
"""
from logging import getLogger

from fastapi import FastAPI, Request

log = getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {"message": "Hello World"}

@app.post("/whatsapp/incoming")
async def whatsapp_incoming(request: Request):
    """
    This is the webhook for incoming messages.
    """
    log.info("request: %s", request.json())

    data = {"message": "Sismos API (reply)"}

    log.info(data)

    return data

@app.post("/whatsapp/status")
async def whatsapp_status(request: Request):
    """
    This is the webhook for status updates.
    """
    log.info("request: %s", request.json())

    data = {"message": "Sismos API (status)"}

    log.info(data)

    return data
