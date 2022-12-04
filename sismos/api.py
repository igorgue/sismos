"""
api.py

This is the api for the webhooks of Twilio's WhatsApp API.
"""
from fastapi import FastAPI, Request

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
    print(f"request: {await request.form()}")

    data = {"message": "Sismos API (reply)"}

    print(data)

    return data

@app.post("/whatsapp/status")
async def whatsapp_status(request: Request):
    """
    This is the webhook for status updates.
    """
    print(f"request: {await request.form()}")

    data = {"message": "Sismos API (status)"}

    print(data)

    return data
