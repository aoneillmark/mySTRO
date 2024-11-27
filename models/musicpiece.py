from Blueprint.library import database as db


class MusicPiece(db.Model):
    __tablename__ = "music_piece"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    composer = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=True)
