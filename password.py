from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from yourapp import db  # Import your SQLAlchemy instance

password_bp = Blueprint('password', __name__)

@password_bp.route('/set_password', methods=['GET', 'POST'])
@login_required
def set_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            hashed_password = generate_password_hash(new_password)
            current_user.password_hash = hashed_password
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('profile'))  # Redirect to profile or another appropriate page
        else:
            flash('Passwords do not match', 'error')

    return render_template('password_setting.html')
