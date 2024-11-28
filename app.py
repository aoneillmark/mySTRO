from flask import Flask, render_template, request
import requests
#from database import db as database

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

# Updated upstream
# # Database initialisation -------------------------------------------------------
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database initialisation -------------------------------------------------------
'''
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
>>>>>>> Stashed changes

# # Set up extensions
# database.init_app(app)

# # Register blueprints
# import Blueprint as blueprints

# app.register_blueprint(blueprints.library)

# # Register cli commands
# from cli import create_all, drop_all, populate

<<<<<<< Updated upstream
# with app.app_context():
#     app.cli.add_command(create_all)
#     app.cli.add_command(drop_all)
#     app.cli.add_command(populate)
# # -------------------------------------------------------------------------------
=======
with app.app_context():
    app.cli.add_command(create_all)
    app.cli.add_command(drop_all)
    app.cli.add_command(populate)'''
# -------------------------------------------------------------------------------


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

   genres = [
       "Keyboard",
       "Orchestral", 
       "Chamber",
       "Stage",
       "Choral",
       "Opera",
       "Vocal"
   ]
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
    selected_composer_id = request.form.get("composer_id")
    name = request.form.get("name")
    selected_genres = request.form.getlist("genres") if request.form.getlist("genres") else [request.form.get("genre")]

    if not selected_composer_id:
        return "No composer selected. Please try again."
    if not selected_genres:
        return "No genres selected. Please try again."

    # Get composer name
    composer_url = f"https://api.openopus.org/composer/list/ids/{selected_composer_id}.json"
    composer_response = requests.get(composer_url)
    composer_name = "Unknown Composer"
    if composer_response.status_code == 200:
        composer_data = composer_response.json()
        composer_name = composer_data.get("composers", [{}])[0].get("complete_name", "Unknown Composer")

    works_url = f"https://api.openopus.org/work/list/composer/{selected_composer_id}/genre/all.json"
    response = requests.get(works_url)

    works = []
    if response.status_code == 200:
        data = response.json()
        all_works = data.get("works", [])
        works = [
            {
                "title": work.get("title", ""),
                "genre": work.get("genre", ""),
                "subtitle": work.get("subtitle", ""),
                "popular": work.get("popular") == "1",
                "recommended": work.get("recommended") == "1",
            }
            for work in all_works
            if work.get("genre") in selected_genres
        ]
    else:
        return f"Failed to fetch works. Status Code: {response.status_code}"

    return render_template(
        "results.html",
        composer_id=selected_composer_id,
        composer_name=composer_name,
        genres=selected_genres,
        name=name,
        works=works
    )

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8000)
