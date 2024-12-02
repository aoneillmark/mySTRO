import pytest
from urllib.parse import quote, unquote


def test_email_share_url():
    """Test email share URL structure"""
    subject = "My Classical Music Collection on MySTRO"
    body = "Hi!\n\nCheck out my classical music collection"
    mailto_url = f"mailto:?subject={quote(subject)}&body={quote(body)}"

    assert mailto_url.startswith("mailto:?subject=")
    assert quote(subject) in mailto_url
    assert quote(body) in mailto_url
