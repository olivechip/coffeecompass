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

    uc_statuses = db.relationship('UserCoffeeshopStatus', backref='user')
    coffeeshops = db.relationship('Coffeeshop', secondary='uc_status', backref='user')

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
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False, unique=True)
    yelp_id = db.Column(db.String, nullable=False, unique=True)

    @classmethod
    def add_to_db(cls, name, address, yelp_id):
        b = Coffeeshop(
            name = name,
            address = address,
            yelp_id = yelp_id
        )
        db.session.add(b)
        return b

class UserCoffeeshopStatus(db.Model):
    __tablename__ = "uc_status"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)
    coffeeshop_id = db.Column(db.Integer, db.ForeignKey('coffeeshops.id', ondelete="cascade"), primary_key=True)
    status = db.Column(db.String)

