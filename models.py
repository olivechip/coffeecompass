from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect the database to the Flask app."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model for storing user account information."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    uc_statuses = db.relationship('UserCoffeeshopStatus', back_populates='user', cascade="all, delete-orphan")

    @classmethod
    def validate_username(cls, username):
        """Validate if the username already exists in the database."""
        return not cls.query.filter_by(username=username).first()

    @classmethod
    def signup(cls, username, password):
        """Create a new user with a hashed password."""
        hashed = bcrypt.generate_password_hash(password).decode('utf8')
        user = cls(username=username, password=hashed)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user using username and password."""
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False

class Coffeeshop(db.Model):
    """Coffeeshop model for storing coffee shop information."""
    __tablename__ = 'coffeeshops'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    yelp_id = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    display_address = db.Column(db.String, nullable=False, unique=True) 
    display_phone = db.Column(db.String, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    review_count = db.Column(db.Integer, default=0) 
    img_url = db.Column(db.String, nullable=True)  # Add img_url column

    uc_statuses = db.relationship('UserCoffeeshopStatus', back_populates='coffeeshop')

    @classmethod
    def add_to_db(cls, name, display_address, yelp_id, display_phone, review_count, rating=None, img_url=None):
        """
        Add a new coffeeshop to the database or 
        update an existing one if the yelp_id already exists.
        """
        shop = cls.query.filter_by(yelp_id=yelp_id).first()
        if shop:
            shop.name = name
            shop.display_address = display_address
            shop.display_phone = display_phone
            shop.rating = rating
            shop.review_count = review_count
            shop.img_url = img_url  # Update img_url
        else:
            shop = cls(
                yelp_id=yelp_id, 
                name=name, 
                display_address=display_address, 
                display_phone=display_phone, 
                rating=rating,
                review_count=review_count,
                img_url=img_url  # Include img_url for new shops
            )
            db.session.add(shop)
        db.session.commit()
        return shop

class UserCoffeeshopStatus(db.Model):
    """Model for tracking user statuses with coffeeshops."""
    __tablename__ = "uc_status"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)
    coffeeshop_id = db.Column(db.Integer, db.ForeignKey('coffeeshops.id', ondelete="cascade"), primary_key=True)
    status = db.Column(db.String, nullable=False)

    user = db.relationship('User', back_populates='uc_statuses')
    coffeeshop = db.relationship('Coffeeshop', back_populates='uc_statuses')

