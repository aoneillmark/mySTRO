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


@click.command(
    "populate", help="Populate the database with initial data"
)  # Maybe this is placeholder?
@with_appcontext
def populate():
    initial_music_pieces = [
        MusicPiece(
            id=1,
            composer="Ludwig van Beethoven",
            title="PLACEHOLDER Sonata No. 14",
            subtitle="Moonlight Sonata",
            genre="Classical",
            popular=True,
            recommended=True,
        ),
        MusicPiece(
            id=2,
            composer="Johann Sebastian Bach",
            title="PLACEHOLDER obscure piece",
            subtitle="who even knows this one",
            genre="Classical",
            popular=False,
            recommended=False,
        ),
    ]
    for piece in initial_music_pieces:
        database.session.add(piece)
    database.session.commit()
