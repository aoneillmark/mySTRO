import pytest
import requests
import os
import urllib.parse
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def test_open_opus_composer_api():
    """Test OpenOpus composer list API."""
    url = "https://api.openopus.org/composer/list/pop.json"
    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()
    assert "composers" in data
    assert isinstance(data["composers"], list)
    assert len(data["composers"]) > 0


def test_open_opus_work_api():
    """Test OpenOpus works list API."""
    composer_id = "145"  # Mozart's ID
    url = "https://api.openopus.org/work/list/composer/" f"{composer_id}/genre/all.json"
    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()
    assert "works" in data
    assert isinstance(data["works"], list)
    assert len(data["works"]) > 0


def test_weather_api():
    """Test Weather API functionality."""
    url = (
        f"http://api.weatherapi.com/v1/current.json?"
        f"key={WEATHER_API_KEY}&q=London&aqi=no"
    )
    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()

    # Check required fields
    assert "location" in data
    assert "current" in data

    # Check location data
    assert "name" in data["location"]
    assert data["location"]["name"] == "London"

    # Check weather data
    assert "temp_c" in data["current"]
    assert "condition" in data["current"]
    assert "text" in data["current"]["condition"]

    # Validate data types
    assert isinstance(data["current"]["temp_c"], (int, float))
    assert isinstance(data["current"]["condition"]["text"], str)


def test_gemini_api_music_description():
    """Test Gemini API for music description generation."""
    # Configure Gemini
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")

    # Test piece info
    test_piece = {
        "title": "Symphony No. 5",
        "composer": "Beethoven",
        "genre": "Symphony",
    }

    # Create prompt
    prompt = (
        f"Give a brief 2-3 sentence description of the classical music piece "
        f"'{test_piece['title']}' by {test_piece['composer']}. "
        f"Consider that it is a {test_piece['genre']} work. "
        f"Focus on its historical significance and emotional impact."
    )

    # Generate response
    response = model.generate_content(prompt)

    # Assertions
    assert response is not None
    assert isinstance(response.text, str)
    assert len(response.text) > 0

    # Check if response contains key elements
    assert any(
        word in response.text.lower()
        for word in [test_piece["title"].lower(), test_piece["composer"].lower()]
    )


def test_gemini_api_weather_suggestion():
    """Test Gemini API for weather-based music suggestions."""
    # Configure Gemini
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")

    # Test weather conditions
    weather_desc = "Sunny"
    temp = 22
    composers = ["Mozart", "Beethoven", "Bach"]

    # Create prompt
    prompt = (
        f"Given that it's {weather_desc} and {temp}°C in London today, "
        f"suggest a classical music piece that would complement this weather. "
        f"Consider selecting from works by these composers: "
        f"{', '.join(composers)}. "
        f"Explain briefly why this piece fits the current weather and mood. "
        f"Keep your response concise but engaging."
    )

    # Generate response
    response = model.generate_content(prompt)

    # Assertions
    assert response is not None
    assert isinstance(response.text, str)
    assert len(response.text) > 0

    # Check if response mentions weather or composer
    response_lower = response.text.lower()
    weather_mood_mentioned = any(
        [
            weather_desc.lower() in response_lower,
            "weather" in response_lower,
            "mood" in response_lower,
        ]
    )
    composer_mentioned = any(
        composer.lower() in response_lower for composer in composers
    )
    assert weather_mood_mentioned or composer_mentioned


def test_youtube_search_url():
    """Test YouTube search URL generation and accessibility."""
    # Test piece info
    test_piece = {
        "composer_name": "Mozart",
        "title": "Symphony No. 40",
        "subtitle": "in G minor",
    }

    # Build search query like in the template
    search_query = (
        f"{test_piece['composer_name']} {test_piece['title']} "
        f"{test_piece.get('subtitle', '')}"
    )
    encoded_query = urllib.parse.quote(search_query)

    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    # Test URL accessibility
    response = requests.get(url)
    assert response.status_code == 200

    # Verify URL structure
    assert "youtube.com/results" in url
    assert "search_query" in url
    assert test_piece["composer_name"] in urllib.parse.unquote(url)
    assert test_piece["title"] in urllib.parse.unquote(url)
    assert test_piece["subtitle"] in urllib.parse.unquote(url)


def test_youtube_search_url_no_subtitle():
    """Test YouTube search URL generation without subtitle."""
    test_piece = {"composer_name": "Beethoven", "title": "Symphony No. 5"}

    # Build search query without subtitle
    search_query = f"{test_piece['composer_name']} {test_piece['title']}"
    encoded_query = urllib.parse.quote(search_query)

    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    # Test URL accessibility
    response = requests.get(url)
    assert response.status_code == 200

    # Verify URL structure
    assert "youtube.com/results" in url
    assert "search_query" in url
    assert test_piece["composer_name"] in urllib.parse.unquote(url)
    assert test_piece["title"] in urllib.parse.unquote(url)


def test_youtube_search_url_special_characters():
    """Test YouTube search URL generation with special characters."""
    test_piece = {
        "composer_name": "Dvořák",
        "title": "Symphony No. 9",
        "subtitle": "From the New World",
    }

    # Build search query
    search_query = (
        f"{test_piece['composer_name']} {test_piece['title']} "
        f"{test_piece.get('subtitle', '')}"
    )
    encoded_query = urllib.parse.quote(search_query)

    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    # Test URL accessibility
    response = requests.get(url)
    assert response.status_code == 200

    # Verify URL encoding
    assert urllib.parse.unquote(encoded_query) == search_query


@pytest.mark.skip(reason="API key required")
def test_weather_api_invalid_key():
    """Test Weather API with invalid key."""
    url = "http://api.weatherapi.com/v1/current.json?" "key=invalid_key&q=London&aqi=no"
    response = requests.get(url)
    assert response.status_code == 401  # Unauthorized


@pytest.mark.skip(reason="API key required")
def test_gemini_api_invalid_key():
    """Test Gemini API with invalid key."""
    try:
        genai.configure(api_key="invalid_key")
        model = genai.GenerativeModel("gemini-pro")
        model.generate_content("Test prompt")  # Removed response assignment
        assert False, "Should have raised an error"
    except Exception as e:
        assert "API key" in str(e).lower() or "authentication" in str(e).lower()
