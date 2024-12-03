from database import db


# Setup of UserLibrary Class
class UserLibrary(db.Model):
    __tablename__ = "user_library"

    # Columns
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    music_piece_id = db.Column(
        db.Integer, db.ForeignKey("music_pieces.id"), primary_key=True
    )

    # Relationship between User and UserLibrary models
    user = db.relationship("User", backref="library")
    music_piece = db.relationship("MusicPiece", backref="libraries")

    # String representation
    def __repr__(self):
        return (
            f"<UserLibrary User {self.user_id}, " f"MusicPiece {self.music_piece_id}>"
        )
