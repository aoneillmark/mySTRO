import requests

API_KEY = "AIzaSyAORVbxFvweoVZ7lOf76JJgyicJhsvu72MY"
URL = "https://www.googleapis.com/youtube/v3/search"
params = {
    "part": "snippet",
    "q": "classical music",
    "key": API_KEY
}

response = requests.get(URL, params=params)
print(response.json())