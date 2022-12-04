"""
api.py

This is the api for the webhooks of Twilio's WhatsApp API.
"""
from fastapi import FastAPI, Request, Response

from . import bot

app = FastAPI()


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {"message": "Hello World"}


@app.post("/whatsapp/incoming")
async def whatsapp_incoming(request: Request) -> Response:
    """
    This is the webhook for incoming messages.
    """
    message = str((await request.form()).get("Body", ""))

    response = bot.respond(message)

    return Response(response, media_type="application/xml")


@app.post("/whatsapp/status")
async def whatsapp_status(request: Request):
    """
    This is the webhook for status updates.
    """
    data = await request.form()

    print(data)
    # print(f"message: {(await request.form())['Body']}")
    #
    # data = {"message": "Sismos API (status)"}

    return {}
