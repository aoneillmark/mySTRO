import click
from flask import Flask, render_template, request
import requests
from database import db as database  # SQLAlchemy database instance

# from models.musicpiece import MusicPiece
import os
from dotenv import load_dotenv
import google.generativeai as genai  # Google Generative AI
import Blueprint as blueprints  # Custom blueprints
from cli import create_all, drop_all, populate  # Custom CLI commands
from flask_session import Session

# Load environment variables
load_dotenv()


# Initialize Flask application
app = Flask(__name__, template_folder="src/templates", static_folder="src/static")


# Database initialization and configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mystro.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["WEATHER_API_KEY"] = os.getenv("WEATHER_API_KEY")
app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
app.config["SESSION_TYPE"] = "filesystem"
genai.configure(api_key=app.config["GOOGLE_API_KEY"])

Session(app)

database.init_app(app)
app.register_blueprint(blueprints.library)


with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)
    click.echo("CLI commands registered")


# Helper functions --------------------------------------------

# Routes ------------------------------------------------------


@app.route("/")
def hello_world():
    return render_template("about.html")


@app.route("/form", methods=["GET", "POST"])
def form():
    composers_url = "https://api.openopus.org/composer/list/name/all.json"
    response = requests.get(composers_url)
    composers = []  # Default to empty list if API call fails

    if response.status_code == 200:
        composers_data = response.json()  # Parse JSON response
        composers = composers_data.get("composers", [])
        # Fetch composer data
    else:
        return f"Failed to fetch composers. Status Code: {response.status_code}"

    genres = ["Keyboard", "Orchestral", "Chamber", "Stage", "Choral", "Opera", "Vocal"]
    return render_template("form.html", composers=composers, genres=genres)


@app.route("/weather-mood")
def weather_mood():
    # Weather API URL with dynamic query for London
    weather_url = (
        "http://api.weatherapi.com/v1/current.json"
        f"?key={app.config['WEATHER_API_KEY']}&q=London&aqi=no"
    )

    try:
        weather_response = requests.get(weather_url)
        weather_data = (
            weather_response.json() if weather_response.status_code == 200 else None
        )

        if weather_data:
            composers_url = "https://api.openopus.org/composer/list/pop.json"
            composers_response = requests.get(composers_url)
            composers = []

            if composers_response.status_code == 200:
                response_data = composers_response.json()
                composers_list = response_data.get("composers", [])
                composers = composers_list[:5]

            # Get weather details step by step
            weather_current = weather_data.get("current", {})
            weather_condition = weather_current.get("condition", {})
            weather_desc = weather_condition.get("text", "")
            temp = weather_current.get("temp_c", 0)

            # Prepare composer names
            composer_names = [composer.get("complete_name") for composer in composers]
            model = genai.GenerativeModel("gemini-pro")

            # Build prompt parts
            weather_part = f"Given that it's {weather_desc} and {temp}°C"
            location_part = "in London today,"
            request_part = (
                "suggest a classical music piece that "
                "would complement "
                "this weather."
            )
            composer_part = (
                "Consider selecting from works by these composers: "
                f"{', '.join(composer_names)}."
            )
            instruction_part = (
                "Explain briefly why this piece fits "
                "the current weather "
                "and mood."
            )
            ending_part = "Keep your response concise but engaging."

            prompt = (
                f"{weather_part} {location_part} {request_part} "
                f"{composer_part} {instruction_part} {ending_part}"
            )

            response = model.generate_content(prompt)
            suggestion = response.text
        else:
            suggestion = None

    except Exception as e:
        print(f"Error: {e}")  # Log errors
        weather_data = None
        suggestion = None

    return render_template(
        "weather_mood.html", weather=weather_data, suggestion=suggestion
    )


@app.route("/search", methods=["POST"])
def search():
    selected_composer_ids = request.form.getlist("composer_id")
    name = request.form.get("name")
    selected_genres = request.form.getlist("genres")

    if not selected_composer_ids:
        return "No composer selected. Please try again."
    if not selected_genres:
        return "No genres selected. Please try again."

    all_works = []  # Hold matching works

    for composer_id in selected_composer_ids:
        composer_url = (
            "https://api.openopus.org/composer/list/" f"ids/{composer_id}.json"
        )
        composer_response = requests.get(composer_url)
        composer_name = "Unknown Composer"

        if composer_response.status_code == 200:
            composer_data = composer_response.json()
            composer_name = composer_data.get("composers", [{}])[0].get(
                "complete_name", "Unknown Composer"
            )

        works_url = (
            "https://api.openopus.org/work/list/composer/"
            f"{composer_id}/genre/all.json"
        )
        response = requests.get(works_url)

        if response.status_code == 200:
            data = response.json()
            composer_works = data.get("works", [])
            filtered_works = [
                {
                    "title": work.get("title", ""),
                    "genre": work.get("genre", ""),
                    "subtitle": work.get("subtitle", ""),
                    "popular": work.get("popular") == "1",
                    "recommended": work.get("recommended") == "1",
                    "composer_name": composer_name,
                    "composer_id": composer_id,
                }
                for work in composer_works
                if work.get("genre") in selected_genres
            ]
            all_works.extend(filtered_works)

    unique_composers = sorted(list(set(work["composer_name"] for work in all_works)))

    return render_template(
        "results.html", name=name, works=all_works, composers=unique_composers
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)