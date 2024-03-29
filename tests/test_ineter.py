"""
test_ineter.py

This is the test for the INETER's "API".
"""
from os import path

from sismos.ineter import parse_html

BASE_DIR = path.dirname(path.abspath(__file__))


def test_parse_html():
    """
    tests the function that parses the html content from ineter.
    """
    content = _get_test_content("sismos.0.php.html")
    items = parse_html(content)

    assert len(items) == 147, "There should be 147 items"

    first = items[0]

    # "22/12/04 16:06:29", "The datetime should be correct"
    assert first["created"].year == 2022, "The year should be 2022"
    assert first["created"].month == 12, "The month should be 12"
    assert first["created"].day == 4, "The day should be 4"
    assert first["created"].hour == 16, "The hour should be 16"
    assert first["created"].minute == 6, "The minute should be 6"
    assert first["created"].second == 29, "The second should be 29"
    assert first["lat"] == "12.590", "The latitude should be correct"
    assert first["long"] == "-90.132", "The longitude should be correct"
    assert first["depth"] == "5", "The depth should be correct"
    assert first["richter"] == "4.1", "The richter should be correct"
    assert first["description"] == "C", "The description should be correct"
    assert (
        first["location"] == "116 Km al sur de Acajutla"
    ), "The location should be correct"
    assert first["country"] == "El Salvador", "The country should be correct"
    assert (
        first["content_hash"]
        == "617216bf36050c6911b92a9d492b7625fa1c13e5e8f971e5b7e1a5bd1bac2778"
    ), "The content hash should be correct"


def _get_test_content(filename: str) -> str:
    """
    Get the test content.
    """
    content = ""
    full_path = path.join(BASE_DIR, "data", filename)

    with open(full_path, "r", encoding="utf-8") as file:
        content = file.read()

    assert content, "Content is empty"

    return content
