import sys
import os

# Add project root to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from flask import Flask
from database import db
from models.musicpiece import MusicPiece
from cli import create_all, drop_all, populate
from sqlalchemy import inspect


@pytest.fixture
def app():
    """Create test Flask application with in-memory SQLite database."""
    flask_app = Flask(__name__)
    # Use in-memory SQLite for test isolation
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()  # Create tables before each test
        yield flask_app  # Run the test
        db.drop_all()  # Clean up after test


def test_create_music_piece(app):
    """Test creating and saving a new music piece."""
    with app.app_context():
        # Create test music piece with all required fields
        piece = MusicPiece(
            title="Symphony No. 5",
            composer="Beethoven",
            genre="Orchestral",
            subtitle="Fate",
            popular=True,
            recommended=True,
            user_name="test_user"
        )
        db.session.add(piece)
        db.session.commit()

        # Verify all fields were saved correctly
        assert piece.id is not None
        assert piece.title == "Symphony No. 5"
        assert piece.subtitle == "Fate"
        assert piece.popular is True
        assert piece.recommended is True
        assert piece.user_name == "test_user"


def test_read_music_piece(app):
    """Test retrieving a music piece from database."""
    with app.app_context():
        # Create and save test piece
        piece = MusicPiece(
            title="Moonlight Sonata",
            composer="Beethoven",
            genre="Piano",
            subtitle="Quasi una fantasia",
            popular=True,
            recommended=False,
            user_name="test_user"
        )
        db.session.add(piece)
        db.session.commit()

        # Test retrieving the saved piece
        retrieved_piece = MusicPiece.query.filter_by(title="Moonlight Sonata").first()
        assert retrieved_piece is not None
        assert retrieved_piece.composer == "Beethoven"
        assert retrieved_piece.subtitle == "Quasi una fantasia"
        assert retrieved_piece.popular is True
        assert retrieved_piece.recommended is False
        assert retrieved_piece.user_name == "test_user"


def test_update_music_piece(app):
    """Test updating an existing music piece."""
    with app.app_context():
        # Create initial piece
        piece = MusicPiece(
            title="Original Title",
            composer="Mozart",
            genre="Chamber",
            subtitle="Old Subtitle",
            popular=False,
            recommended=False,
            user_name="test_user"
        )
        db.session.add(piece)
        db.session.commit()

        # Update multiple fields
        piece.title = "New Title"
        piece.subtitle = "New Subtitle"
        piece.popular = True
        db.session.commit()

        # Verify updates were saved
        updated_piece = db.session.get(MusicPiece, piece.id)
        assert updated_piece.title == "New Title"
        assert updated_piece.subtitle == "New Subtitle"
        assert updated_piece.popular is True
        assert updated_piece.user_name == "test_user"


def test_delete_music_piece(app):
    """Test deleting a music piece."""
    with app.app_context():
        # Create a piece to delete
        piece = MusicPiece(
            title="To Delete",
            composer="Bach",
            genre="Choral",
            subtitle="Test",
            popular=True,
            recommended=True,
            user_name="test_user"
        )
        db.session.add(piece)
        db.session.commit()

        # Delete the piece
        db.session.delete(piece)
        db.session.commit()

        # Verify piece was deleted
        deleted_piece = db.session.get(MusicPiece, piece.id)
        assert deleted_piece is None


def test_database_creation(app):
    """Test database table creation."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Use SQLAlchemy inspector to check if table exists
        inspector = inspect(db.engine)
        assert 'music_piece' in inspector.get_table_names()


def test_database_population(app):
    """Test populating database with initial data."""
    with app.app_context():
        db.create_all()
        # Create initial test pieces
        initial_music_pieces = [
            MusicPiece(
                id=1,
                composer="Ludwig van Beethoven",
                title="PLACEHOLDER Sonata No. 14",
                subtitle="Moonlight Sonata",
                genre="Classical",
                popular=True,
                recommended=True,
                user_name="test_user"
            ),
            MusicPiece(
                id=2,
                composer="Johann Sebastian Bach",
                title="PLACEHOLDER obscure piece",
                subtitle="who even knows this one",
                genre="Classical",
                popular=False,
                recommended=False,
                user_name="test_user"
            ),
        ]
        # Add and save pieces
        for piece in initial_music_pieces:
            db.session.add(piece)
        db.session.commit()

        # Verify population
        pieces = MusicPiece.query.all()
        assert len(pieces) == 2