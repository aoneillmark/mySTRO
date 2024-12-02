import pytest
import requests
from urllib.parse import quote, unquote


def test_twitter_share_url():
    """Test Twitter share URL generation"""
    base_url = "https://twitter.com/intent/tweet"
    text = "Classical music gems on MySTRO 🎵"
    encoded_text = quote(text)
    share_url = f"{base_url}?text={encoded_text}"

    # Test URL accessibility
    response = requests.get(share_url)
    assert response.status_code == 200
    assert unquote(share_url).endswith(text)
