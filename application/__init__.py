from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# creating Flask instance
app = Flask(__name__)

# secret key to prevent CSRF
app.config["SECRET_KEY"] = "a4eeabd90111471121f4cee081c0d913"
#  database SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
# for hashing passwords          
bcrypt = Bcrypt()
# login manager
login_manager = LoginManager(app)
# redirects to login page whenever login is required
login_manager.login_view = "login"

from application import routes
