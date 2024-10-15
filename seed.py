from app import db
from models import User

db.drop_all()
db.create_all()

user1 = User.signup('user1', 'password')
user2 = User.signup('user2', 'password')
db.session.commit()

print("Database has been reset and seeded with new users.")
