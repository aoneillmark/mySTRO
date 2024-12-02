from database import db


# Setup of MusicPiece Class
class MusicPiece(db.Model):
    __tablename__ = "music_pieces"

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    composer = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    subtitle = db.Column(db.String(80), nullable=True)
    genre = db.Column(db.String(80), nullable=False)
    popular = db.Column(db.Boolean, nullable=False)
    recommended = db.Column(db.Boolean, nullable=False)

    # Checking for unique entries
    __table_args__ = (
        db.UniqueConstraint(
            "composer", "title", "subtitle", name="unique_music_piece"
        ),
    )

    # String representation
    def __repr__(self):
        return f"<MusicPiece {self.id}: {self.title} by {self.composer}>"
