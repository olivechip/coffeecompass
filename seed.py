from app import db
from models import User

db.drop_all()
db.create_all()

user = User.register('changarooboy@gmail.com', 'changarooboy', 'password')
db.session.commit()

