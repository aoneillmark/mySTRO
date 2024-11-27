from flask import Flask
from database import db

# import Blueprint as blueprints
from models import MusicPiece

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db.init_app(app)

with app.app_context():
    # Check if the database exists
    tables = db.engine.table_names()
    print("Tables:", tables)

    # Query all music pieces
    all_pieces = db.session.query(MusicPiece).all()
    for piece in all_pieces:
        print(f"Title: {piece.title}, Composer: {piece.composer}, Genre: {piece.genre}, Description: {piece.description}")