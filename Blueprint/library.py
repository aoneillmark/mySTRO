from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import select
import google.generativeai as genai

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


@library.route("/add_piece", methods=["GET", "POST"])
def add_piece():
    """
    Add a new music piece to the library.
    """
    composer = request.form.get("composer_name")
    title = request.form.get("title")
    subtitle = request.form.get("subtitle")
    genre = request.form.get("genre")
    popular = request.form.get("popular") == "true"
    recommended = request.form.get("recommended") == "true"

    new_piece = MusicPiece(
        composer=composer,
        title=title,
        subtitle=subtitle,
        genre=genre,
        popular=popular,
        recommended=recommended,
    )

    database.session.add(new_piece)
    database.session.commit()

    return redirect(url_for("library.all_pieces"))


@library.route("/<int:piece_id>", methods=["GET", "POST"])
def single_piece(piece_id):
    """
    View or delete a single music piece.
    """
    music_piece = database.get_or_404(
        MusicPiece, piece_id, description="Music piece not found."
    )

    # Generate AI description
    ai_description = None
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Give a brief 2-3 sentence description of the classical music piece '{music_piece.title}' by {music_piece.composer}. Consider that it is a {music_piece.genre} work. Focus on its historical significance and emotional impact."
        response = model.generate_content(prompt)
        ai_description = response.text
    except Exception as e:
        print(f"Error generating AI description: {e}")

    if request.method == "POST":
        # Handle delete action
        if request.form.get("submit_button") == "delete":
            database.session.delete(music_piece)
            database.session.commit()
            return redirect(url_for("library.all_pieces"))

    return render_template("library_piece.html", piece=music_piece, ai_description=ai_description)