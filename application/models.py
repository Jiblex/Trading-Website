from application import db, login_manager
from flask_login import UserMixin


# function gets user by user's id, decorator lets extension know this is the function to use to get user by id
@login_manager.user_loader
def load_user(user_id):
    # get user id, casting to int to avoid errors
    return User.query.get(int(user_id))


# Class represents a user in the database with all of their information
# Inheriting from UserMixin to not have to add the 4 attributes manually (is_authenticated, is_active ...): manages
# sessions for us
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    profile_img = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    # printed format of User
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_img}')"
