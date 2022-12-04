"""
test_ineter.py

This is the test for the INETER's "API".
"""
from sismos.ineter import parse_html


def test_parse_html():
    """
    tests the function that parses the html content from ineter.
    """
    content = _get_test_content()

    data = parse_html(content)

    assert data, "Data is empty"


def _get_test_content() -> str:
    """
    Get the test content.
    """
    content = ""
    with open("tests/data/sismos.php.html", "r", encoding="utf-8") as file:
        content = file.read()

    assert content, "Content is empty"

    return content
