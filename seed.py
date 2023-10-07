from app import db
from models import User

db.drop_all()
db.create_all()

user = User.signup('changarooboy', 'password', "/static/images/default-pic.png")
db.session.commit()

