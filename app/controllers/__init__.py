from flask.ext.login import LoginManager
from ..models import User
from app import app

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
