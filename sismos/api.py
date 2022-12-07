"""
api.py

This is the api for the webhooks of Twilio's WhatsApp API.
"""
from fastapi import Depends, FastAPI, Request, Response
from sqlalchemy.orm import Session

from sismos.database import SessionLocal
from sismos.models import Sismo

from . import bot

app = FastAPI()

# Dependency
def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()  # pylint: disable=invalid-name
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root(db: Session = Depends(get_db)):  # pylint: disable=invalid-name
    """
    Root endpoint.
    """
    return Sismo.latest(db)


@app.post("/whatsapp/incoming")
async def whatsapp_incoming(
    request: Request, db: Session = Depends(get_db)  # pylint: disable=invalid-name
) -> Response:
    """
    This is the webhook for incoming messages.
    """
    message = str((await request.form()).get("Body", ""))
    message = _sql_safe(message)

    response = bot.respond_with_ai(db, message)

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


def _sql_safe(text: str) -> str:
    """
    Make the given text safe for SQL.
    """
    return text.replace("'", "''").replace('"', "")
