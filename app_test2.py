import pytest
from app import app
import requests_mock


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    with requests_mock.Mocker() as mock:
        composers_url = "https://api.openopus.org/composer/list/name/all.json"
        mock.get(composers_url, json={"composers": [{"id": 1, "name": "Mozart", "epoch": "Classical"}]})

        response = client.get("/form")
        assert response.status_code == 200
        # Adjust test to check for composer and epoch without requiring exact formatting
        assert b'Mozart (Classical)' in response.data


def test_composer_api_failure(client):
    with requests_mock.Mocker() as mock:
        composers_url = "https://api.openopus.org/composer/list/name/all.json"
        mock.get(composers_url, status_code=500)

        response = client.get("/form")
        assert response.status_code == 200
        assert b"Failed to fetch composers" in response.data


def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200
    # Check for a specific heading in the about.html content
    assert b"About MySTRO" in response.data


def test_search_route(client):
    with requests_mock.Mocker() as mock:
        # Mock the 'works' API endpoint
        works_url = "https://api.openopus.org/work/list/composer/1/genre/all.json"
        mock.get(works_url, json={"works": [{"id": 1, "title": "Symphony No. 1", "genre": "Orchestral"}]})

        # Mock the 'composer' API endpoint
        composer_url = "https://api.openopus.org/composer/list/ids/1.json"
        mock.get(composer_url, json={"composers": [{"id": 1, "complete_name": "Wolfgang Amadeus Mozart"}]})

        form_data = {
            "composer_id": "1",
            "name": "Mozart",
            "genres": ["Orchestral"]  # Ensure 'genres' is a list
        }
        response = client.post("/search", data=form_data)
        assert response.status_code == 200
        assert b"Symphony No. 1" in response.data


def test_search_genre_validation(client):
    form_data = {"composer_id": "1", "name": "Mozart"}  # Missing genre
    response = client.post("/search", data=form_data)
    assert response.status_code == 200
    assert b"No genres selected. Please try again." in response.data


def test_search_composer_validation(client):
    form_data = {"genre": "Orchestral"}  # Missing composer_id
    response = client.post("/search", data=form_data)
    assert response.status_code == 200
    assert b"No composer selected" in response.data