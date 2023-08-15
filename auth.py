# auth.py

# Dummy user data (replace this with your authentication logic)
users = {
    'admin': 'admin',
    'username2': 'password2'
}

def authenticate_user(username, password):
    print(f"Received username: {username}, password: {password}")
    if users.get(username) == password:
        return True
    return False
# ... (your existing code)
def is_admin(username):
    return users.get(username) == 'admin'

