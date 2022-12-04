"""
ineter.py

This is the API for the INETER's "API".
"""
import httpx
from bs4 import BeautifulSoup


DATA_URL = "https://webserver2.ineter.gob.ni/geofisica/sis/events/sismos.php"


def get_lines_from_api() -> list[str]:
    """
    Get the lines from the INETER's "API".
    """
    content = _fetch_data()

    return parse_html(content)


def parse_html(content: str) -> list[str]:
    """
    Get the lines from the INETER's "API".
    """
    soup = BeautifulSoup(content, "html.parser")
    pres = list(soup.find_all("pre"))

    return [pre.text for pre in pres]


def _fetch_data() -> str:
    """
    Do the request to the INETER's "API".
    """
    return httpx.get(DATA_URL).text
