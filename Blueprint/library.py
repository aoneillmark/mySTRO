from flask import Blueprint, render_template, redirect, url_for, request
from database import db
from models.musicpiece import MusicPiece
from models.user import User
from models.userlibrary import UserLibrary

# Define Blueprint for the library
library = Blueprint("library", __name__, url_prefix="/library")

# Route to display user's music library
@library.route("/", methods=["GET"])
def all_pieces():
   user_name = request.args.get("user_name")

   if not user_name:
       return render_template("library.html", pieces=[], username_missing=True)

   user = User.query.filter_by(username=user_name).first()

   if not user:
       return render_template("library.html", pieces=[], username_missing=False, user_name=user_name)

   user_pieces = [entry.music_piece for entry in user.library]

   return render_template("library.html", pieces=user_pieces, username_missing=False, user_name=user_name)

# Route to add new music piece to the user's library
@library.route("/add_piece", methods=["GET", "POST"])
def add_piece():
   # Get the user, music piece, and related information from the form
   user_name = request.form.get("user_name")
   composer = request.form.get("composer_name")
   title = request.form.get("title")
   subtitle = request.form.get("subtitle")
   genre = request.form.get("genre")
   popular = request.form.get("popular") == "true"
   recommended = request.form.get("recommended") == "true"

   # Find the user, or create new one if not found
   user = User.query.filter_by(username=user_name).first()
   if not user:
       user = User(username=user_name)
       db.session.add(user)
       db.session.commit()

   # Find the music piece, or create new one if not found
   music_piece = MusicPiece.query.filter_by(composer=composer, title=title, subtitle=subtitle).first()
   if not music_piece:
       music_piece = MusicPiece(composer=composer, title=title, subtitle=subtitle, genre=genre, popular=popular, recommended=recommended)
       db.session.add(music_piece)
       db.session.commit()

   # Check if music piece is already in user's library, and add it if not
   existing_entry = UserLibrary.query.filter_by(user_id=user.id, music_piece_id=music_piece.id).first()
   if not existing_entry:
       user_library_entry = UserLibrary(user_id=user.id, music_piece_id=music_piece.id)
       db.session.add(user_library_entry)
       db.session.commit()
   else:
       print(f"Music piece '{title}' by '{composer}' is already in the library.")

   # Redirect to user's library
   return redirect(url_for("library.all_pieces", user_name=user_name))

# Function to delete music pieces not referenced by any user library
def delete_orphaned_music_pieces():
   orphaned_pieces = (
       db.session.query(MusicPiece)
       .outerjoin(UserLibrary, MusicPiece.id == UserLibrary.music_piece_id)
       .filter(UserLibrary.music_piece_id == None)
       .all()
   )

   for piece in orphaned_pieces:
       db.session.delete(piece)
   db.session.commit()

# Route to view or remove a single music piece from a user's library
@library.route("/<int:piece_id>", methods=["GET", "POST"])
def single_piece(piece_id):
    user_name = request.args.get("user_name") or request.form.get("user_name")
    if not user_name:
        return "User not found", 404

    user = User.query.filter_by(username=user_name).first()
    if not user:
        return "User not found", 404

    user_library_entry = UserLibrary.query.filter_by(user_id=user.id, music_piece_id=piece_id).first()

    if request.method == "POST" and request.form.get("submit_button") == "delete":
        if user_library_entry:
            db.session.delete(user_library_entry)
            db.session.commit()
            delete_orphaned_music_pieces()
        return redirect(url_for("library.all_pieces", user_name=user_name))

    return render_template("library_piece.html", piece=user_library_entry.music_piece)


# Route to display the library form and handle composer and genre selection
@library.route("/form", methods=["GET", "POST"])
def library_form():
   # Fetch the list of composers from the OpenOpus API
   try:
       response = request.get("https://api.openopus.org/composer/list/name/all.json")
       composers = response.json()["composers"] if response.status_code == 200 else []
   except Exception:
       composers = []

   # Define the list of genres
   genres = ["Keyboard", "Orchestral", "Chamber", "Stage", "Choral", "Opera", "Vocal"]

   return render_template("form.html", composers=composers, genres=genres)