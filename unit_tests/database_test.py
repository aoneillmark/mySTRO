import pytest
from flask import Flask
from database import db
from models.musicpiece import MusicPiece
from cli import create_all, drop_all, populate


# Create a test Flask application with an in-memory database
# So tests are isolated and don't affect the production database
@pytest.fixture
def app():
    flask_app = Flask(__name__)
    # Use in-memory for faster testing and isolation
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()  # Create tables before each test
        yield flask_app  # Run the test
        db.drop_all()  # Clean up after each test


# Test CREATE operation
def test_create_music_piece(app):
    with app.app_context():
        # Create a new music piece with all fields
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

        # Verify all fields were saved correctly
        assert piece.id is not None
        assert piece.title == "Symphony No. 5"
        assert piece.subtitle == "Fate"
        assert piece.popular is True
        assert piece.recommended is True


# Test READ operation
def test_read_music_piece(app):
    with app.app_context():
        # Add test data
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

        # Test retrieving the data
        query = MusicPiece.query
        filtered_query = query.filter_by(title="Moonlight Sonata")
        retrieved_piece = filtered_query.first()
        assert retrieved_piece is not None
        assert retrieved_piece.composer == "Beethoven"
        assert retrieved_piece.subtitle == "Quasi una fantasia"
        assert retrieved_piece.popular is True
        assert retrieved_piece.recommended is False


# Test DELETE operation
def test_delete_music_piece(app):
    with app.app_context():
        # Create a piece to delete
        piece = MusicPiece(
            title="To Delete",
            composer="Bach",
            genre="Choral",
            subtitle="Test",
            popular=True,
            recommended=True,
        )
        db.session.add(piece)
        db.session.commit()

        # Delete the piece
        db.session.delete(piece)
        db.session.commit()

        # Verify piece was deleted
        deleted_piece = MusicPiece.query.get(piece.id)
        assert deleted_piece is None


# Test CLI command for creating database tables
def test_create_all(app):
    with app.app_context():
        create_all()
        # Verify table exists in database
        assert MusicPiece.__table__.exists(db.engine)


# Test CLI command for dropping database tables
def test_drop_all(app):
    with app.app_context():
        create_all()
        drop_all()
        # Verify table was dropped
        assert not MusicPiece.__table__.exists(db.engine)


# Test CLI command for populating initial data
def test_populate(app):
    with app.app_context():
        create_all()
        populate()

        # Verify both initial pieces were added
        pieces = MusicPiece.query.all()
        assert len(pieces) == 2

        # Check Beethoven piece details
        beethoven_piece = MusicPiece.query.filter_by(
            composer="Ludwig van Beethoven"
        ).first()
        assert beethoven_piece.title == "PLACEHOLDER Sonata No. 14"
        assert beethoven_piece.subtitle == "Moonlight Sonata"
        assert beethoven_piece.popular is True

        # Check Bach piece details
        bach_piece = MusicPiece.query.filter_by(
            composer="Johann Sebastian Bach"
        ).first()
        assert bach_piece.title == "PLACEHOLDER obscure piece"
        assert bach_piece.recommended is False
