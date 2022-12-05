"""
ineter.py

This is the API for the INETER's "API".
"""
import httpx
from bs4 import BeautifulSoup

DATA_URL = "https://webserver2.ineter.gob.ni/geofisica/sis/events/sismos.php"


def get_lines_from_api() -> list[dict]:
    """
    Get the lines from the INETER's "API".
    """
    content = _fetch_data()

    return parse_html(content)


def parse_html(content: str) -> list[dict]:
    """
    Get the lines from the INETER's "API".
    """
    soup = BeautifulSoup(content, "html.parser")
    pres = list(soup.find_all("pre"))

    return [_parse_pre(pre.text) for pre in pres]


def _parse_pre(pre: str) -> dict:
    """
    Parse the pre tag.
    """
    parts = pre.split()

    local_time = " ".join(parts[0:2])
    lat, long = parts[2:4]
    depth = parts[4]
    richter = parts[5]
    description = parts[6]
    location = " ".join(parts[7:])

    return {
        "datetime": local_time,
        "lat": lat,
        "long": long,
        "depth": depth,
        "richter": richter,
        "description": description,
        "location": location,
    }


def _fetch_data() -> str:
    """
    Do the request to the INETER's "API".
    """
    return httpx.get(DATA_URL).text
