# auth.py

# Dummy user data (replace this with your authentication logic)
users = {
    'username1': 'password1',
    'username2': 'password2'
}

def authenticate_user(username, password):
    if users.get(username) == password:
        return True
    return False
