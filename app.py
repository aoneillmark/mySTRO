import click
from flask import Flask, render_template, request
import requests
from database import db as database
import os
from dotenv import load_dotenv
import google.generativeai as genai
import Blueprint as blueprints
from cli import create_all, drop_all, populate
from flask_session import Session
    
def create_app(testing=False):
    # Initialize Flask application
    app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
    
    if testing:
        # Test configuration
        app.config.update({
            'TESTING': True,
            'SECRET_KEY': 'test_key',
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'WEATHER_API_KEY': 'test_key',
            'GOOGLE_API_KEY': 'test_key'
        })
        database.init_app(app)
        app.register_blueprint(blueprints.library)  # Add this line
        register_routes(app)
        return app
        
    # Rest of your code...
        
    # Production configuration
    load_dotenv()
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///mystro.db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WEATHER_API_KEY": os.getenv("WEATHER_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "SESSION_TYPE": "filesystem"
    })
    
    genai.configure(api_key=app.config["GOOGLE_API_KEY"])
    Session(app)
    database.init_app(app)
    app.register_blueprint(blueprints.library)

    # Register CLI commands
    with app.app_context():
        app.cli.add_command(create_all)
        app.cli.add_command(drop_all)
        app.cli.add_command(populate)
        click.echo("CLI commands registered")

    register_routes(app)
    return app
        
    # Production configuration
    load_dotenv()
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///mystro.db",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WEATHER_API_KEY": os.getenv("WEATHER_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "SESSION_TYPE": "filesystem"
    })
    
    genai.configure(api_key=app.config["GOOGLE_API_KEY"])
    Session(app)
    database.init_app(app)
    app.register_blueprint(blueprints.library)

    # Register CLI commands
    with app.app_context():
        app.cli.add_command(create_all)
        app.cli.add_command(drop_all)
        app.cli.add_command(populate)
        click.echo("CLI commands registered")

    register_routes(app)
    return app

def register_routes(app):
    @app.route("/")
    def hello_world():
        return render_template("about.html")

    @app.route("/form", methods=["GET", "POST"])
    def form():
        composers_url = "https://api.openopus.org/composer/list/name/all.json"
        response = requests.get(composers_url)
        composers = []
        all_works = []  # Initialize all_works here

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

        genres = ["Keyboard", "Orchestral", "Chamber", "Stage", "Choral", "Opera", "Vocal"]
        return render_template("form.html", composers=composers, genres=genres)

    @app.route("/weather-mood")
    def weather_mood():
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

                weather_current = weather_data.get("current", {})
                weather_condition = weather_current.get("condition", {})
                weather_desc = weather_condition.get("text", "")
                temp = weather_current.get("temp_c", 0)

                composer_names = [composer.get("complete_name") for composer in composers]
                model = genai.GenerativeModel("gemini-pro")

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

        for composer_id in selected_composer_ids:
            composer_url = (
                "https://api.openopus.org/composer/list/"
                f"ids/{composer_id}.json"
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
            else:
                return render_template("noresults.html")

        unique_composers = sorted(list(set(work["composer_name"] for work in all_works)))

        return render_template(
            "results.html", name=name, works=all_works, composers=unique_composers
        )

# Only create the production app if running directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)