from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import select

from database import db as database
from models.musicpiece import MusicPiece

# Define the Blueprint for the library
library = Blueprint("library", __name__, url_prefix="/library")


@library.route("/", methods=["GET"])
def all_pieces():
    """
    Display all music pieces in the user's library.
    """
    all_pieces = database.session.execute(select(MusicPiece)).scalars().all()
    return render_template("library.html", pieces=all_pieces)


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