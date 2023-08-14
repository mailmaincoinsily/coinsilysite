from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from .user import User

auth_bp = Blueprint('auth', __name__)

# Mocked user database (replace with a proper database in a real app)
users = {'username': {'password_hash': generate_password_hash('password')}}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            user = User(username, users[username]['password_hash'])
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Incorrect password', 'error')
        else:
            flash('User not found', 'error')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
