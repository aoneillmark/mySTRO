import click
from flask import Flask, render_template, request
import requests
from database import db as database
from models.musicpiece import MusicPiece

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

# Databse initialisation -------------------------------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mystro.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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

# Print to verify database has worked
@app.route('/library')
def get_music_pieces():
    pieces = MusicPiece.query.all()
    return render_template("library.html", pieces=pieces)


# # -------------------------------------------------------------------------------


@app.route("/form", methods=["GET", "POST"])
def home():
    # Load the list of composers
    composers_url = "https://api.openopus.org/composer/list/name/all.json"
    response = requests.get(composers_url)


    composers = []
    if response.status_code == 200:
        composers_data = response.json()
        composers = composers_data.get("composers", [])
    else:
        return f"Failed to fetch composers. Status Code: {response.status_code}"

    # Updated genres
    genres = [
        "Keyboard",
        "Orchestral",
        "Chamber",
        "Stage",
        "Choral",
        "Opera",
        "Vocal"
    ]
    # Render the form with the list of composers and genres
    return render_template("form.html", composers=composers, genres=genres)

@app.route("/")
def hello_world():
    return render_template("about.html")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/library")
def library():
    return render_template("library.html")

@app.route("/search", methods=["POST"])
def search():
    print("Form Data:", request.form)

    # Get selected composer and genre from the form
    selected_composer_id = request.form.get("composer_id")
    selected_genre = request.form.get("genre")

    if not selected_composer_id:
        return "No composer selected. Please try again."
    if not selected_genre:
        return "No genre selected. Please try again."

    # Fetch works from the API
    works_url = f"https://api.openopus.org/work/list/composer/{selected_composer_id}/genre/all.json"
    response = requests.get(works_url)

    works = []
    if response.status_code == 200:
        data = response.json()
        all_works = data.get("works", [])
        # Filter works by the selected genre
        works = [work for work in all_works if work.get("genre") == selected_genre]
    else:
        return f"Failed to fetch works for composer ID {selected_composer_id}. Status Code: {response.status_code}"

    # Render results page
    return render_template(
        "results.html",
        composer_id=selected_composer_id,
        genre=selected_genre,
        works=works
    )
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
