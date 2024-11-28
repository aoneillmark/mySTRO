from database import db


class MusicPiece(db.Model):
    __tablename__ = "music_piece"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    composer = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=True)

    def __repr__(self): # just like overloading the toString method in C++
        return f"<MusicPiece {self.id}: {self.title} by {self.composer}>"