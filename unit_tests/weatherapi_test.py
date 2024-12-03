import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests_mock
from unittest.mock import Mock, patch
from app import create_app


@pytest.fixture
def app():
    test_app = create_app(testing=True)
    return test_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_weather_mood_integration(client):
    with requests_mock.Mocker() as mock:
        # Mock weather API with complete response structure
        mock.get(
            "http://api.weatherapi.com/v1/current.json?key=test_key&q=London&aqi=no",
            json={
                "location": {
                    "name": "London",
                    "region": "City of London",
                    "country": "United Kingdom",
                },
                "current": {
                    "condition": {"text": "Sunny"},
                    "temp_c": 20,
                    "last_updated": "2024-03-20 13:00",
                },
            },
        )
        # Mock composers API
        mock.get(
            "https://api.openopus.org/composer/list/pop.json",
            json={"composers": [{"complete_name": "Mozart"}]},
        )

        # Mock Gemini response
        with patch("google.generativeai.GenerativeModel") as mock_genai:
            mock_model = Mock()
            mock_model.generate_content.return_value.text = "Test music suggestion"
            mock_genai.return_value = mock_model

            response = client.get("/weather-mood")
            assert response.status_code == 200
            assert b"London" in response.data
            assert b"Sunny" in response.data
            assert b"20" in response.data


def test_weather_api_failure(client):
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://api.weatherapi.com/v1/current.json?key=test_key&q=London&aqi=no",
            status_code=500,
        )

        response = client.get("/weather-mood")
        assert response.status_code == 200
        # Verify template renders with no weather data
        assert b"weather-mood" in response.data.lower()
