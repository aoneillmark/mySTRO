import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests_mock
from app import create_app

@pytest.fixture
def app():
    test_app = create_app(testing=True)
    return test_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_form_route_composers_success(client):
    with requests_mock.Mocker() as mock:
        mock.get(
            "https://api.openopus.org/composer/list/name/all.json",
            json={"composers": [{"id": 1, "name": "Mozart", "epoch": "Classical"}]}
        )
        response = client.get("/form")
        assert response.status_code == 200
        assert b'Mozart' in response.data
        assert b'Classical' in response.data

# ... rest of your tests ...

def test_form_route_composers_failure(client):
    with requests_mock.Mocker() as mock:
        mock.get(
            "https://api.openopus.org/composer/list/name/all.json",
            status_code=500
        )
        response = client.get("/form")
        assert response.status_code == 200
        assert b"Failed to fetch composers" in response.data

def test_search_works_integration(client):
    with requests_mock.Mocker() as mock:
        # Mock composer details endpoint
        mock.get(
            "https://api.openopus.org/composer/list/ids/1.json",
            json={"composers": [{"complete_name": "Wolfgang Amadeus Mozart"}]}
        )
        # Mock works endpoint
        mock.get(
            "https://api.openopus.org/work/list/composer/1/genre/all.json",
            json={
                "works": [{
                    "title": "Symphony No. 40",
                    "genre": "Orchestral",
                    "subtitle": "Great",
                    "popular": "1",
                    "recommended": "1"
                }]
            }
        )
        
        form_data = {
            "composer_id": ["1"],
            "name": "Mozart",
            "genres": ["Orchestral"]
        }
        response = client.post("/search", data=form_data)
        assert response.status_code == 200
        # Check for the presence of the work details
        assert b"Symphony No. 40" in response.data
        assert b"Mozart" in response.data
        assert b"Orchestral" in response.data