from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
