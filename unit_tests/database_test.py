import pytest
from flask import Flask
from database import db
from models.musicpiece import MusicPiece
from cli import create_all, drop_all, populate


@pytest.fixture
def app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


def test_create_music_piece(app):
    with app.app_context():
        piece = MusicPiece(
            title="Symphony No. 5",
            composer="Beethoven",
            genre="Orchestral",
            subtitle="Fate",
            popular=True,
            recommended=True,
            user_name="test_user"  # Added required field
        )
        db.session.add(piece)
        db.session.commit()

        assert piece.id is not None
        assert piece.title == "Symphony No. 5"


def test_read_music_piece(app):
    with app.app_context():
        piece = MusicPiece(
            title="Moonlight Sonata",
            composer="Beethoven",
            genre="Piano",
            subtitle="Quasi una fantasia",
            popular=True,
            recommended=False,
            user_name="test_user"  # Added required field
        )
        db.session.add(piece)
        db.session.commit()

        retrieved_piece = MusicPiece.query.filter_by(title="Moonlight Sonata").first()
        assert retrieved_piece is not None
        assert retrieved_piece.composer == "Beethoven"


def test_update_music_piece(app):
    with app.app_context():
        piece = MusicPiece(
            title="Original Title",
            composer="Mozart",
            genre="Chamber",
            subtitle="Old Subtitle",
            popular=False,
            recommended=False,
            user_name="test_user"  # Added required field
        )
        db.session.add(piece)
        db.session.commit()

        piece.title = "New Title"
        db.session.commit()

        updated_piece = MusicPiece.query.get(piece.id)
        assert updated_piece.title == "New Title"


def test_delete_music_piece(app):
    with app.app_context():
        piece = MusicPiece(
            title="To Delete",
            composer="Bach",
            genre="Choral",
            subtitle="Test",
            popular=True,
            recommended=True,
            user_name="test_user"  # Added required field
        )
        db.session.add(piece)
        db.session.commit()

        db.session.delete(piece)
        db.session.commit()

        deleted_piece = MusicPiece.query.get(piece.id)
        assert deleted_piece is None


# For CLI commands, directly call the database functions instead of Click commands
def test_database_creation(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        assert MusicPiece.__table__.exists(db.engine)


def test_database_population(app):
    with app.app_context():
        db.create_all()
        populate()

        pieces = MusicPiece.query.all()
        assert len(pieces) == 2

        beethoven_piece = MusicPiece.query.filter_by(composer="Ludwig van Beethoven").first()
        assert beethoven_piece is not None
        assert beethoven_piece.title == "PLACEHOLDER Sonata No. 14"
