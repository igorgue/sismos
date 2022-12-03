"""
api.py

This is the api for the webhooks of Twilio's WhatsApp API.
"""
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/whatsapp/incoming")
def whatsapp_incoming(request: Request):
    """
    This is the webhook for incoming messages.
    """
    return request.json()

@app.post("/whatsapp/status")
def whatsapp_status(request: Request):
    """
    This is the webhook for status updates.
    """
    return request.json()
