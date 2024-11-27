import click
from flask.cli import with_appcontext

from database import db as database
from models.musicpiece import MusicPiece


@click.command("create_all", help="Create all tables in the app's databases")
@with_appcontext
def create_all():
    database.create_all()

@click.command("drop_all", help="Drop all tables in the specified database")
@with_appcontext
def drop_all():
    database.drop_all()


@click.command("populate", help="Populate the database with initial data") # Maybe this is placeholder?
@with_appcontext
def populate():
    initial_music_pieces = [
        MusicPiece(
            id = 1,
            title="PLACEHOLDER Sonata No. 14",
            composer="Ludwig van Beethoven",
            genre="Classical",
            description="A beautiful piano sonata composed by Beethoven. :3",
        ),
        MusicPiece(
            id = 2,
            title="PLACEHOLDER Symphony No. 5",
            composer="Ludwig van Beethoven",
            genre="Classical",
            description="A symphony composed by Beethoven.",
        )
    ]
    for piece in initial_music_pieces:
        database.session.add(piece)
    database.session.commit()