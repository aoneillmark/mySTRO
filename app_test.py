import pytest
from app import app as flask_app
from database import db
from models.musicpiece import MusicPiece


@pytest.fixture
def app():
    """Create a new Flask app instance for testing."""
    flask_app.config.from_object("test_config.TestConfig")

    with flask_app.app_context():
        db.create_all()  # Initialize the in-memory database
        yield flask_app  # Provide the app instance to tests
        db.session.remove()
        db.drop_all()  # Clean up after tests


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def sample_music_piece():
    """Create a sample music piece for testing."""
    return MusicPiece(
        title="Symphony No. 1",
        composer="Ludwig van Beethoven",
        genre="Orchestral",
        year=1800,
    )


def test_database_insert(app, sample_music_piece):
    """Test inserting a music piece into the database."""
    with app.app_context():
        db.session.add(sample_music_piece)
        db.session.commit()

        # Check if the record exists
        piece = MusicPiece.query.filter_by(title="Symphony No. 1").first()
        assert piece is not None
        assert piece.composer == "Ludwig van Beethoven"
        assert piece.genre == "Orchestral"


def test_database_query(app, sample_music_piece):
    """Test querying the database."""
    with app.app_context():
        db.session.add(sample_music_piece)
        db.session.commit()

        # Query by composer
        pieces = MusicPiece.query.filter_by(composer="Ludwig van Beethoven").all()
        assert len(pieces) == 1
        assert pieces[0].title == "Symphony No. 1"


def test_database_update(app, sample_music_piece):
    """Test updating a database record."""
    with app.app_context():
        db.session.add(sample_music_piece)
        db.session.commit()

        # Update the record
        piece = MusicPiece.query.filter_by(title="Symphony No. 1").first()
        piece.year = 1801
        db.session.commit()

        # Verify the update
        updated_piece = MusicPiece.query.filter_by(title="Symphony No. 1").first()
        assert updated_piece.year == 1801


def test_database_delete(app, sample_music_piece):
    """Test deleting a database record."""
    with app.app_context():
        db.session.add(sample_music_piece)
        db.session.commit()

        # Delete the record
        piece = MusicPiece.query.filter_by(title="Symphony No. 1").first()
        db.session.delete(piece)
        db.session.commit()

        # Verify deletion
        deleted_piece = MusicPiece.query.filter_by(title="Symphony No. 1").first()
        assert deleted_piece is None