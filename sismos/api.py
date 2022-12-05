"""
api.py

This is the api for the webhooks of Twilio's WhatsApp API.
"""
from fastapi import Depends, FastAPI, Request, Response
from sqlalchemy.orm import Session

from sismos.database import SessionLocal

from . import bot

app = FastAPI()

# Dependency
def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {"message": "Hello World"}


@app.post("/whatsapp/incoming")
async def whatsapp_incoming(
    request: Request, db: Session = Depends(get_db)  # pylint: disable=invalid-name
) -> Response:
    """
    This is the webhook for incoming messages.
    """
    message = str((await request.form()).get("Body", ""))

    response = bot.respond(db, message)

    return Response(response, media_type="application/xml")


@app.post("/whatsapp/status")
async def whatsapp_status(request: Request):
    """
    This is the webhook for status updates.
    """
    # TODO: Do this thing
    data = await request.form()

    print(data)

    return {}
