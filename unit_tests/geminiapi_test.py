import pytest
import requests
import os
import urllib.parse
from dotenv import load_dotenv
import google.generativeai as genai
import requests_mock
from unittest.mock import Mock, patch

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def test_gemini_api_music_description():
    # Test Gemini API for music description generation.
    with patch("google.generativeai.GenerativeModel") as mock_genai:
        # Create mock response
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = (
            "Beethoven's Symphony No. 5 is a groundbreaking work that exemplifies "
            "the composer's profound musical genius. The piece's majestic themes "
            "and dramatic shifts in mood capture the full range of human emotion, "
            "from triumphant heroism to deep introspection."
        )
        mock_model.generate_content.return_value = mock_response
        mock_genai.return_value = mock_model

        # Configure and test
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-pro")

        test_piece = {
            "title": "Symphony No. 5",
            "composer": "Beethoven",
            "genre": "Symphony",
        }

        prompt = (
            f"Give a brief 2 sentence description of the music piece "
            f"'{test_piece['title']}' by {test_piece['composer']}. "
            f"Consider that it is a {test_piece['genre']} work. "
            f"Focus on its historical significance and emotional impact."
        )

        response = model.generate_content(prompt)

        assert response is not None
        assert isinstance(response.text, str)
        assert len(response.text) > 0
        assert "Beethoven" in response.text
        assert "Symphony No. 5" in response.text


def test_gemini_api_weather_suggestion():
    # Test Gemini API for weather-based music suggestions.
    with patch("google.generativeai.GenerativeModel") as mock_genai:
        # Create mock response
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = (
            "Suggested classical music piece: Beethoven's 'Pastoral Symphony'. "
            "This piece captures the serene, peaceful mood of a sunny day with "
            "its flowing melodies and pastoral themes."
        )
        mock_model.generate_content.return_value = mock_response
        mock_genai.return_value = mock_model

        # Configure and test
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-pro")

        weather_desc = "Sunny"
        temp = 22
        composers = ["Mozart", "Beethoven", "Bach"]

        prompt = (
            f"Given that it's {weather_desc} and {temp}°C in London today, "
            f"suggest a classical music piece that would complement this weather. "
            f"Consider selecting from works by these composers: "
            f"{', '.join(composers)}. "
            f"Explain briefly why this piece fits the current weather and mood. "
            f"Keep your response concise but engaging."
        )

        response = model.generate_content(prompt)

        assert response is not None
        assert isinstance(response.text, str)
        assert len(response.text) > 0
        assert "Beethoven" in response.text
        assert "Pastoral Symphony" in response.text
        assert "serene, peaceful mood" in response.text


def test_gemini_api_error_handling():
    # Test Gemini API error handling.
    with patch("google.generativeai.GenerativeModel") as mock_genai:
        # Setup mock to raise an exception
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.return_value = mock_model

        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-pro")

        test_piece = {
            "title": "Invalid Piece",
            "composer": "Test Composer",
            "genre": "Test Genre",
        }

        prompt = f"Test prompt for {test_piece['title']}"

        with pytest.raises(Exception) as exc_info:
            model.generate_content(prompt)

        assert "API Error" in str(exc_info.value)


def test_gemini_api_prompt_formatting():
    # Test prompt formatting for Gemini API.
    test_cases = [
        {
            "weather": {"desc": "Sunny", "temp": 25},
            "composers": ["Mozart", "Beethoven"],
            "expected_keywords": ["Sunny", "25°C", "Mozart", "Beethoven"],
        },
        {
            "weather": {"desc": "Rainy", "temp": 15},
            "composers": ["Bach", "Chopin"],
            "expected_keywords": ["Rainy", "15°C", "Bach", "Chopin"],
        },
    ]

    for case in test_cases:
        prompt = (
            f"Given that it's {case['weather']['desc']} and "
            f"{case['weather']['temp']}°C in London today, "
            f"suggest a classical music piece that would complement this weather. "
            f"Consider selecting from works by these composers: "
            f"{', '.join(case['composers'])}. "
            f"Explain briefly why this piece fits the current weather and mood. "
            f"Keep your response concise but engaging."
        )

        for keyword in case["expected_keywords"]:
            assert keyword in prompt
