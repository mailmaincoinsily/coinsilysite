from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

password_bp = Blueprint('password', __name__, url_prefix='/password')

@password_bp.route('/set', methods=['GET', 'POST'])
@login_required
def set_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            current_user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash('Password successfully set!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Passwords do not match.', 'error')

    return render_template('password.html')
