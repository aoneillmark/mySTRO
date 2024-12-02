import pytest
import requests
import os
import urllib.parse
import requests_mock


def test_youtube_search_url():
    # Test URL generation and accessibility
    test_piece = {
        "composer_name": "Mozart",
        "title": "Symphony No. 40",
        "subtitle": "in G minor",
    }

    search_query = (
        f"{test_piece['composer_name']} {test_piece['title']} "
        f"{test_piece.get('subtitle', '')}"
    )
    encoded_query = urllib.parse.quote(search_query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    with requests_mock.Mocker() as mock:
        # Mock YouTube response
        mock.get(url, text="<html>Mocked YouTube Results</html>")
        response = requests.get(url)
        assert response.status_code == 200

    # Verify URL structure
    assert "youtube.com/results" in url
    assert "search_query" in url
    assert test_piece["composer_name"] in urllib.parse.unquote(url)
    assert test_piece["title"] in urllib.parse.unquote(url)
    assert test_piece["subtitle"] in urllib.parse.unquote(url)


def test_youtube_search_url_no_subtitle():
    # Test URL generation without subtitle
    test_piece = {"composer_name": "Beethoven", "title": "Symphony No. 5"}

    search_query = f"{test_piece['composer_name']} {test_piece['title']}"
    encoded_query = urllib.parse.quote(search_query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    with requests_mock.Mocker() as mock:
        # Mock YouTube response
        mock.get(url, text="<html>Mocked YouTube Results</html>")
        response = requests.get(url)
        assert response.status_code == 200

    # Verify URL structure
    assert "youtube.com/results" in url
    assert "search_query" in url
    assert test_piece["composer_name"] in urllib.parse.unquote(url)
    assert test_piece["title"] in urllib.parse.unquote(url)


def test_youtube_search_url_special_characters():
    # Test URL generation with special characters
    test_piece = {
        "composer_name": "Dvořák",
        "title": "Symphony No. 9",
        "subtitle": "From the New World",
    }

    search_query = (
        f"{test_piece['composer_name']} {test_piece['title']} "
        f"{test_piece.get('subtitle', '')}"
    )
    encoded_query = urllib.parse.quote(search_query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"

    with requests_mock.Mocker() as mock:
        # Mock YouTube response
        mock.get(url, text="<html>Mocked YouTube Results</html>")
        response = requests.get(url)
        assert response.status_code == 200

    # Verify URL encoding
    assert urllib.parse.unquote(encoded_query) == search_query


def test_youtube_search_url_encoding():
    # Test URL encoding and decoding functionality
    test_pieces = [
        {
            "composer_name": "Johann Sebastian Bach",
            "title": "The Well-Tempered Clavier, Book I",
            "subtitle": "BWV 846-869",
        },
        {"composer_name": "Maurice Ravel", "title": "Boléro", "subtitle": "M.81"},
        {
            "composer_name": "Frédéric Chopin",
            "title": "Études, Op. 10",
            "subtitle": "No. 3 in E major 'Tristesse'",
        },
    ]

    for piece in test_pieces:
        search_query = (
            f"{piece['composer_name']} {piece['title']} " f"{piece.get('subtitle', '')}"
        )
        encoded_query = urllib.parse.quote(search_query)
        decoded_query = urllib.parse.unquote(encoded_query)

        assert decoded_query == search_query
        assert " " not in encoded_query
        assert "%20" in encoded_query
