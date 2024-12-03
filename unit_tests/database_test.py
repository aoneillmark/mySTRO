import sys
import os

# Add project root to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from flask import Flask
from database import db
from models.musicpiece import MusicPiece
from models.user import User
from models.userlibrary import UserLibrary
from cli import create_all, drop_all, populate
from sqlalchemy import inspect


@pytest.fixture
def app():
    """Create test Flask application with in-memory SQLite database."""
    flask_app = Flask(__name__)
    # Use in-memory SQLite for test isolation
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()  # Create tables before each test
        yield flask_app  # Run the test
        db.drop_all()  # Clean up after test


def test_create_music_piece(app):
    """Test creating and saving a new music piece."""
    with app.app_context():
        # Create a test user
        user = User(username="test_user")
        db.session.add(user)
        db.session.commit()

        # Create and save a new music piece
        piece = MusicPiece(
            title="Symphony No. 5",
            composer="Beethoven",
            genre="Orchestral",
            subtitle="Fate",
            popular=True,
            recommended=True,
        )
        db.session.add(piece)
        db.session.commit()

        # Link the user and the music piece
        user_library = UserLibrary(user_id=user.id, music_piece_id=piece.id)
        db.session.add(user_library)
        db.session.commit()

        # Verify all fields were saved correctly
        assert piece.id is not None
        assert piece.title == "Symphony No. 5"
        assert piece.subtitle == "Fate"
        assert piece.popular is True
        assert piece.recommended is True

        # Verify the association
        assert user.library[0].music_piece_id == piece.id


def test_read_music_piece(app):
    """Test retrieving a music piece from database."""
    with app.app_context():
        # Create a test user
        user = User(username="test_user")
        db.session.add(user)
        db.session.commit()

        # Create and save a new music piece
        piece = MusicPiece(
            title="Moonlight Sonata",
            composer="Beethoven",
            genre="Piano",
            subtitle="Quasi una fantasia",
            popular=True,
            recommended=False,
        )
        db.session.add(piece)
        db.session.commit()

        # Link the user and the music piece
        user_library = UserLibrary(user_id=user.id, music_piece_id=piece.id)
        db.session.add(user_library)
        db.session.commit()

        # Retrieve the piece
        retrieved_piece = MusicPiece.query.filter_by(title="Moonlight Sonata").first()
        assert retrieved_piece is not None
        assert retrieved_piece.composer == "Beethoven"
        assert retrieved_piece.subtitle == "Quasi una fantasia"
        assert retrieved_piece.popular is True
        assert retrieved_piece.recommended is False


def test_update_music_piece(app):
    """Test updating an existing music piece."""
    with app.app_context():
        # Create a test user
        user = User(username="test_user")
        db.session.add(user)
        db.session.commit()

        # Create and save a new music piece
        piece = MusicPiece(
            title="Original Title",
            composer="Mozart",
            genre="Chamber",
            subtitle="Old Subtitle",
            popular=False,
            recommended=False,
        )
        db.session.add(piece)
        db.session.commit()

        # Link the user and the music piece
        user_library = UserLibrary(user_id=user.id, music_piece_id=piece.id)
        db.session.add(user_library)
        db.session.commit()

        # Update multiple fields
        piece.title = "New Title"
        piece.subtitle = "New Subtitle"
        piece.popular = True
        db.session.commit()

        # Verify updates
        updated_piece = db.session.get(MusicPiece, piece.id)
        assert updated_piece.title == "New Title"
        assert updated_piece.subtitle == "New Subtitle"
        assert updated_piece.popular is True


def delete_orphaned_music_pieces():
    """
    Delete any MusicPiece records that are not referenced by any UserLibrary entry.
    """
    orphaned_pieces = (
        db.session.query(MusicPiece)
        .outerjoin(UserLibrary, MusicPiece.id == UserLibrary.music_piece_id)
        .filter(
            UserLibrary.music_piece_id == None
        )  # Find music pieces with no references
        .all()
    )

    for piece in orphaned_pieces:
        db.session.delete(piece)

    db.session.commit()


def test_delete_music_piece(app):
    """Test removing a music piece from a user's library."""
    with app.app_context():
        # Create two users
        user1 = User(username="user1")
        user2 = User(username="user2")
        db.session.add_all([user1, user2])
        db.session.commit()

        # Create and save a new music piece
        piece = MusicPiece(
            title="Shared Piece",
            composer="Mozart",
            genre="Classical",
            subtitle="Subtitle",
            popular=True,
            recommended=False,
        )
        db.session.add(piece)
        db.session.commit()

        # Link the music piece to both users
        user1_library = UserLibrary(user_id=user1.id, music_piece_id=piece.id)
        user2_library = UserLibrary(user_id=user2.id, music_piece_id=piece.id)
        db.session.add_all([user1_library, user2_library])
        db.session.commit()

        # Remove the music piece from user1's library
        db.session.delete(user1_library)
        db.session.commit()

        # Verify the music piece still exists in the database
        retrieved_piece = db.session.get(MusicPiece, piece.id)
        assert retrieved_piece is not None

        # Verify the music piece is still in user2's library
        remaining_library = UserLibrary.query.filter_by(user_id=user2.id).all()
        assert len(remaining_library) == 1
        assert remaining_library[0].music_piece_id == piece.id

        # Remove the music piece from user2's library
        db.session.delete(user2_library)
        db.session.commit()

        # Call the cleanup function explicitly
        delete_orphaned_music_pieces()

        # Verify the music piece is deleted from the database
        deleted_piece = db.session.get(MusicPiece, piece.id)
        assert deleted_piece is None
