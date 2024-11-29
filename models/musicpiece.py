from database import db


class MusicPiece(db.Model):
    __tablename__ = "music_piece"
    id = db.Column(db.Integer, primary_key=True)
    composer = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    subtitle = db.Column(db.String(80), nullable=True)
    genre = db.Column(db.String(80), nullable=False)
    popular = db.Column(db.Boolean, nullable=False)
    recommended = db.Column(db.Boolean, nullable=False)
    

    def __repr__(self): # just like overloading the toString method in C++
        return f"<MusicPiece {self.id}: {self.title} by {self.composer}>"