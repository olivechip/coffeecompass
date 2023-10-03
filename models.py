from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, default="/static/images/default-pic.png")

    @classmethod
    def validate_username(cls, username):
        if cls.query.filter_by(username=username).first():
            return False
        return True

    @classmethod
    def signup(cls, username, password, image_url):
        hashed = bcrypt.generate_password_hash(password).decode('utf8')
        user = User(
            username = username,
            password = hashed,
            image_url = image_url
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

class Coffeeshop(db.Model):
    __tablename__ = 'coffeeshops'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False, unique=True)