import os

import pytz
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL") or "redis://localhost:6379/0"

app = Celery("tasks", broker=REDIS_URL)
timezone = pytz.timezone("America/Managua")

assert app.on_after_configure is not None


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Tasks to be run periodically.
    """
    # add task to fetch data from the API every 5 minutes
    sender.add_periodic_task(
        crontab(minute="*/5"),
        fetch_sismos_data.s(),
        name="Fetch data every 5 minutes",
    )

    assert kwargs is not None


@app.task
def fetch_sismos_data(arg):
    """
    Fetch data from the INETER's "API"
    """
    print("Fetching data...")

    assert arg