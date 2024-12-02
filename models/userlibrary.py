from database import db

class UserLibrary(db.Model):
    __tablename__ = "user_library"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    music_piece_id = db.Column(db.Integer, db.ForeignKey("music_pieces.id"), primary_key=True)

    user = db.relationship("User", backref="library")
    music_piece = db.relationship("MusicPiece", backref="libraries")

    def __repr__(self):
        return f"<UserLibrary User {self.user_id}, MusicPiece {self.music_piece_id}>"
