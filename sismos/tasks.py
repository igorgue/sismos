"""
tasks.py

Celery tasks that fetch data from the API.
"""
import os

import pytz
from celery import Celery
from dotenv import load_dotenv

from sismos import database, models
from sismos.ineter import get_data_from_api

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379/0"

app = Celery("tasks", broker=REDIS_URL)
timezone = pytz.timezone("America/Managua")

models.Base.metadata.create_all(bind=database.engine)

assert app.on_after_configure is not None


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Tasks to be run periodically.
    """
    # add task to fetch data from the API every 5 minutes
    sender.add_periodic_task(
        5.0 * 60.0,
        fetch_sismos_data.s(),
        name="Fetch data every 5 seconds",
    )

    assert kwargs is not None


@app.task
def fetch_sismos_data():
    """
    Fetch data from the INETER's "API"
    """
    data = get_data_from_api()

    print(f"Adding {len(data)} sismos to the database.")

    models.Sismo.create_from(database.SessionLocal(), data)
