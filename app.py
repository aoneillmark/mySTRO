import click
from flask import Flask, render_template, request
import requests
from database import db as database
from models.musicpiece import MusicPiece
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

# Database initialization and config -------------------------------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mystro.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["WEATHER_API_KEY"] = os.getenv("WEATHER_API_KEY")
app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=app.config["GOOGLE_API_KEY"])

# Set up extensions
database.init_app(app)

# Register blueprints
import Blueprint as blueprints

app.register_blueprint(blueprints.library)

# Register cli commands
from cli import create_all, drop_all, populate

with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)
    click.echo("CLI commands registered")

# Routes -------------------------------------------------------------------------------


@app.route("/library")
def library():
    pieces = MusicPiece.query.all()
    return render_template("library.html", pieces=pieces)


@app.route("/form", methods=["GET", "POST"])
def home():
    composers_url = "https://api.openopus.org/composer/list/name/all.json"
    response = requests.get(composers_url)

    composers = []
    if response.status_code == 200:
        composers_data = response.json()
        composers = composers_data.get("composers", [])
    else:
        return f"Failed to fetch composers. Status Code: {response.status_code}"

    genres = ["Keyboard", "Orchestral", "Chamber", "Stage", "Choral", "Opera", "Vocal"]
    return render_template("form.html", composers=composers, genres=genres)


@app.route("/")
def hello_world():
    return render_template("about.html")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/weather-mood")
def weather_mood():
    weather_url = f"http://api.weatherapi.com/v1/current.json?key={app.config['WEATHER_API_KEY']}&q=London&aqi=no"

    try:
        weather_response = requests.get(weather_url)
        weather_data = (
            weather_response.json() if weather_response.status_code == 200 else None
        )

        if weather_data:
            # Get works from OpenOpus API for context
            composers_url = "https://api.openopus.org/composer/list/pop.json"
            composers_response = requests.get(composers_url)
            composers = []
            if composers_response.status_code == 200:
                composers_data = composers_response.json()
                composers = composers_data.get("composers", [])[
                    :5
                ]  # Get top 5 composers

            weather_desc = weather_data["current"]["condition"]["text"]
            temp = weather_data["current"]["temp_c"]
            composer_names = [c.get("complete_name") for c in composers]

            # Configure Gemini model
            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""Given that it's {weather_desc} and {temp}°C in London today, 
            suggest a classical music piece that would complement this weather. 
            Consider selecting from works by these composers: {', '.join(composer_names)}.
            Explain briefly why this piece fits the current weather and mood.
            Keep your response concise but engaging."""

            # Get Gemini's recommendation
            response = model.generate_content(prompt)
            suggestion = response.text
        else:
            suggestion = None

    except Exception as e:
        print(f"Error: {e}")
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

    all_works = []

    # Get works for each selected composer
    for composer_id in selected_composer_ids:
        # Get composer name
        composer_url = f"https://api.openopus.org/composer/list/ids/{composer_id}.json"
        composer_response = requests.get(composer_url)
        composer_name = "Unknown Composer"

        if composer_response.status_code == 200:
            composer_data = composer_response.json()
            composer_name = composer_data.get("composers", [{}])[0].get(
                "complete_name", "Unknown Composer"
            )

        # Get works
        works_url = (
            f"https://api.openopus.org/work/list/composer/{composer_id}/genre/all.json"
        )
        response = requests.get(works_url)

        if response.status_code == 200:
            data = response.json()
            composer_works = data.get("works", [])
            # Add composer information to each work
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
        else: return render_template("noresults.html")

    # Get unique composer names for filtering
    unique_composers = sorted(list(set(work["composer_name"] for work in all_works)))

    return render_template(
        "results.html", name=name, works=all_works, composers=unique_composers
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
