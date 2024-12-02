# Fixture to create test Flask app instance with an in-memory SQLite database
@pytest.fixture
def app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

# Test creating and saving new music piece
def test_create_music_piece(app):
    with app.app_context():
        user = User(username="test_user")
        db.session.add(user)
        db.session.commit()

        piece = MusicPiece(title="Symphony No. 5", composer="Beethoven", genre="Orchestral", subtitle="Fate", popular=True, recommended=True)
        db.session.add(piece)
        db.session.commit()

        user_library = UserLibrary(user_id=user.id, music_piece_id=piece.id)
        db.session.add(user_library)
        db.session.commit()

        assert piece.id is not None
        assert piece.title == "Symphony No. 5"
        assert piece.subtitle == "Fate"
        assert piece.popular is True
        assert piece.recommended is True
        assert user.library[0].music_piece_id == piece.id

# Test retrieving music piece from the database
def test_read_music_piece(app):
    with app.app_context():
        user = User(username="test_user")
        db.session.add(user)
        db.session.commit()

        piece = MusicPiece(title="Moonlight Sonata", composer="Beethoven", genre="Piano", subtitle="Quasi una fantasia", popular=True, recommended=False)
        db.session.add(piece)
        db.session.commit()

        user_library = UserLibrary(user_id=user.id, music_piece_id=piece.id)
        db.session.add(user_library)
        db.session.commit()

        retrieved_piece = MusicPiece.query.filter_by(title="Moonlight Sonata").first()
        assert retrieved_piece is not None
        assert retrieved_piece.composer == "Beethoven"
        assert retrieved_piece.subtitle == "Quasi una fantasia"
        assert retrieved_piece.popular is True
        assert retrieved_piece.recommended is False

# Test updating existing music piece
def test_update_music_piece(app):
    with app.app_context():
        user = User(username="test_user")
        db.session.add(user)
        db.session.commit()

        piece = MusicPiece(title="Original Title", composer="Mozart", genre="Chamber", subtitle="Old Subtitle", popular=False, recommended=False)
        db.session.add(piece)
        db.session.commit()

        user_library = UserLibrary(user_id=user.id, music_piece_id=piece.id)
        db.session.add(user_library)
        db.session.commit()

        piece.title = "New Title"
        piece.subtitle = "New Subtitle"
        piece.popular = True
        db.session.commit()

        updated_piece = db.session.get(MusicPiece, piece.id)
        assert updated_piece.title == "New Title"
        assert updated_piece.subtitle == "New Subtitle"
        assert updated_piece.popular is True

# Test removing music piece from user's library
def test_delete_music_piece(app):
    with app.app_context():
        user1 = User(username="user1")
        user2 = User(username="user2")
        db.session.add_all([user1, user2])
        db.session.commit()

        piece = MusicPiece(title="Shared Piece", composer="Mozart", genre="Classical", subtitle="Subtitle", popular=True, recommended=False)
        db.session.add(piece)
        db.session.commit()

        user1_library = UserLibrary(user_id=user1.id, music_piece_id=piece.id)
        user2_library = UserLibrary(user_id=user2.id, music_piece_id=piece.id)
        db.session.add_all([user1_library, user2_library])
        db.session.commit()

        db.session.delete(user1_library)
        db.session.commit()

        retrieved_piece = db.session.get(MusicPiece, piece.id)
        assert retrieved_piece is not None

        remaining_library = UserLibrary.query.filter_by(user_id=user2.id).all()
        assert len(remaining_library) == 1
        assert remaining_library[0].music_piece_id == piece.id

        db.session.delete(user2_library)
        db.session.commit()

        delete_orphaned_music_pieces()

        deleted_piece = db.session.get(MusicPiece, piece.id)
        assert deleted_piece is None
