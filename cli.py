import click
from flask.cli import with_appcontext

from database import db as database
from models.musicpiece import MusicPiece


@click.command("create_all", help="Create all tables in the app's databases")
@with_appcontext
def create_all():
    print("Creating all tables in the database...")
    database.create_all()


@click.command("drop_all", help="Drop all tables in the specified database")
@with_appcontext
def drop_all():
    print("Dropping all tables in the database...")
    database.drop_all()


@click.command("populate", help="Populate the database with initial data")
@with_appcontext
def populate():
    print("Populating the database with initial data...")
    initial_music_pieces = [
        MusicPiece(
            title="PLACEHOLDER Sonata No. 14",
            composer="Ludwig van Beethoven",
            genre="Classical",
            description="A beautiful piano sonata composed by Beethoven. :3",
        ),
        MusicPiece(
            title="PLACEHOLDER Symphony No. 5",
            composer="Ludwig van Beethoven",
            genre="Classical",
            description="A symphony composed by Beethoven.",
        ),
    ]
    for piece in initial_music_pieces:
        database.session.add(piece)
    database.session.commit()
    click.echo("Database populated with initial data.")
