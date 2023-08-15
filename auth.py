# auth.py
# Load user data from the JSON file
with open('user_data.json', 'r') as f:
    users = json.load(f)


def authenticate_user(username, password):
    print(f"Received username: {username}, password: {password}")
    if users.get(username) == password:
        return True
    return False
# ... (your existing code)
def is_admin(username):
    return users.get(username) == 'admin'

