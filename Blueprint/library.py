from flask import Blueprint, render_template, redirect
from flask import url_for, request, session
from database import db as database
from models.musicpiece import MusicPiece

# Define the Blueprint for the library
library = Blueprint("library", __name__, url_prefix="/library")


@library.route("/", methods=["GET"])
def all_pieces():
    """
    Display all music pieces in the user's library.
    """
    user_library = session.get("library", [])

    # Ensure all items have an id
    for index, piece in enumerate(user_library):
        if 'id' not in piece:
            piece['id'] = index + 1

    session['library'] = user_library
    session.modified = True

    return render_template("library.html", pieces=user_library)


@library.route("/add_piece", methods=["GET", "POST"])
def add_piece():
    """
    Add a new music piece to the library.
    """
    if request.method == "POST":
        composer = request.form.get("composer_name")
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        genre = request.form.get("genre")
        popular = request.form.get("popular") == "true"
        recommended = request.form.get("recommended") == "true"

        new_piece = {
            "id": len(session.get("library", [])) + 1,  # Assign a unique ID
            "composer": composer,
            "title": title,
            "subtitle": subtitle,
            "genre": genre,
            "popular": popular,
            "recommended": recommended,
        }

        if "library" not in session:
            session["library"] = []

        session["library"].append(new_piece)
        session.modified = True

        return redirect(url_for("library.all_pieces"))

    return render_template("add_piece.html")


@library.route("/<int:piece_id>", methods=["GET", "POST"])
def single_piece(piece_id):
    """
    View or delete a single music piece.
    """
    music_piece = database.get_or_404(
        MusicPiece, piece_id, description="Music piece not found."
    )

    if request.method == "POST":
        # Handle delete action
        if request.form.get("submit_button") == "delete":
            database.session.delete(music_piece)
            database.session.commit()
            return redirect(url_for("library.all_pieces"))

    return render_template("library_piece.html", piece=music_piece)
