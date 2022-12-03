"""
whatsapp.py

This is the api for the webhooks of Twilio's WhatsApp API.
"""
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/whatsapp")
