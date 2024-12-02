import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import requests_mock
from app import create_app


# Fixture to create testing Flask app instance
@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


# Fixture to create test client for the Flask app
@pytest.fixture
def client(app):
    return app.test_client()


# Test root route ("/")
def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"About MySTRO" in response.data


# Test form route ("/form")
def test_form_route_basic(client):
    response = client.get("/form")
    assert response.status_code == 200

    # Check if all expected genres are present in the response
    expected_genres = [b"Keyboard", b"Orchestral", b"Chamber",
                       b"Stage", b"Choral", b"Opera", b"Vocal"]
    for genre in expected_genres:
        assert genre in response.data


# Test search validation errors
def test_search_validation_errors(client):
    # Define test cases with expected error messages
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

    # Run test cases and assert the expected error messages
    for form_data, expected_message in test_cases:
        response = client.post("/search", data=form_data)
        assert response.status_code == 200
        assert expected_message in response.data