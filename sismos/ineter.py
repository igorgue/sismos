"""
ineter.py

This is the API for the INETER's "API".
"""
from datetime import datetime
from hashlib import sha256

import httpx
import pytz
from bs4 import BeautifulSoup

DATA_URL = "https://webserver2.ineter.gob.ni/geofisica/sis/events/sismos.php"

timezone = pytz.timezone("America/Managua")


def get_data_from_api() -> list[dict]:
    """
    Get the lines from the INETER's "API".
    """
    content = _fetch_data()

    return parse_html(content)


def hash_content(pre: str) -> str:
    """
    Generate a hash from the pre tag.
    """
    return sha256(pre.encode()).hexdigest()


def parse_html(content: str) -> list[dict]:
    """
    Get the lines from the INETER's "API".
    """
    soup = BeautifulSoup(content, "html.parser")
    pres = list(soup.find_all("pre"))

    return [parse_pre_item(pre.text) for pre in pres]


def parse_pre_item(pre: str) -> dict:
    """
    Parse the pre tag.
    """
    pre = pre.strip()

    content_hash = hash_content(pre)

    parts = pre.split()

    local_time = " ".join(parts[0:2])
    lat, long = parts[2:4]
    depth = parts[4]
    richter = parts[5]
    description = parts[6]
    location = " ".join(parts[7:])
    country = location.rsplit(", ", maxsplit=1)[-1]
    location = location.replace(f", {country}", "")

    # parse "22/12/04 16:06:29" to datetime
    created = datetime.strptime(local_time, "%y/%m/%d %H:%M:%S").replace(
        tzinfo=timezone
    )

    data = {
        "created": created,
        "lat": lat,
        "long": long,
        "depth": depth,
        "richter": richter,
        "description": description,
        "location": location,
        "content_hash": content_hash,
        "country": country,
    }

    return data


def _fetch_data() -> str:
    """
    Do the request to the INETER's "API".
    """
    return httpx.get(DATA_URL).text
