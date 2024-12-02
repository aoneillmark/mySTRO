import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy import inspect
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
            user_name="test_user"
        )
        db.session.add(piece)
        db.session.commit()

        assert piece.id is not None
        assert piece.title == "Symphony No. 5"
        assert piece.subtitle == "Fate"
        assert piece.popular is True
        assert piece.recommended is True
        assert piece.user_name == "test_user"


def test_read_music_piece(app):
    with app.app_context():
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

        retrieved_piece = MusicPiece.query.filter_by(title="Moonlight Sonata").first()
        assert retrieved_piece is not None
        assert retrieved_piece.composer == "Beethoven"
        assert retrieved_piece.subtitle == "Quasi una fantasia"
        assert retrieved_piece.popular is True
        assert retrieved_piece.recommended is False
        assert retrieved_piece.user_name == "test_user"


def test_update_music_piece(app):
    with app.app_context():
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

        piece.title = "New Title"
        piece.subtitle = "New Subtitle"
        piece.popular = True
        db.session.commit()

        updated_piece = db.session.get(MusicPiece, piece.id)
        assert updated_piece.title == "New Title"
        assert updated_piece.subtitle == "New Subtitle"
        assert updated_piece.popular is True
        assert updated_piece.user_name == "test_user"


def test_delete_music_piece(app):
    with app.app_context():
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

        db.session.delete(piece)
        db.session.commit()

        deleted_piece = db.session.get(MusicPiece, piece.id)
        assert deleted_piece is None

def test_database_creation(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        inspector = inspect(db.engine)
        assert 'music_piece' in inspector.get_table_names()

def test_database_population(app):
    with app.app_context():
        db.create_all()
        # Call populate function directly
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
        for piece in initial_music_pieces:
            db.session.add(piece)
        db.session.commit()

        pieces = MusicPiece.query.all()
        assert len(pieces) == 2