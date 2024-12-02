import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests_mock
from app import create_app  # Import create_app instead of app

@pytest.fixture
def app():
    app = create_app(testing=True)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"About MySTRO" in response.data

def test_form_route_basic(client):
    """Test that form route exists and returns expected genres"""
    response = client.get("/form")
    assert response.status_code == 200
    # Check if all genres are present
    expected_genres = [b"Keyboard", b"Orchestral", b"Chamber", 
                      b"Stage", b"Choral", b"Opera", b"Vocal"]
    for genre in expected_genres:
        assert genre in response.data

def test_search_validation_errors(client):
    test_cases = [
        (
            {"genres": ["Orchestral"]},  # Missing composer_id
            b"No composer selected"
        ),
        (
            {"composer_id": ["1"], "name": "Mozart"},  # Missing genres
            b"No genres selected"
        )
    ]
    
    for form_data, expected_message in test_cases:
        response = client.post("/search", data=form_data)
        assert response.status_code == 200
        assert expected_message in response.data