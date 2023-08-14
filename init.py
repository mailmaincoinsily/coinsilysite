from flask_login import LoginManager
from .user import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username, users[username]['password_hash'])
    return None
