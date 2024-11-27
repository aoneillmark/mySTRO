from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")


@app.route("/form", methods=["GET", "POST"])
def home():
    # Load the list of composers
    api_url = "https://api.openopus.org/composer/list/name/all.json"  # Change this if you find a broader endpoint
    response = requests.get(api_url)

    composers = []
    if response.status_code == 200:
        data = response.json()
        composers = data.get("composers", [])
    else:
        return f"Failed to fetch composers. Status Code: {response.status_code}"

    # Render the form with the list of composers
    return render_template("form.html", composers=composers)


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
    # Get the composer ID from the form
    selected_composer_id = request.form.get("composer_id")

    if not selected_composer_id:
        return "No composer selected. Please try again."

    # Fetch the works of the selected composer using their ID
    works_url = f"https://api.openopus.org/work/list/composer/{selected_composer_id}/genre/all.json"
    response = requests.get(works_url)

    works = []
    if response.status_code == 200:
        data = response.json()
        works = data.get("works", [])
    else:
        return f"Failed to fetch works for composer ID {selected_composer_id}. Status Code: {response.status_code}"

    # Render the results page
    return render_template(
        "results.html",
        composer_id=selected_composer_id,
        works=works
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
