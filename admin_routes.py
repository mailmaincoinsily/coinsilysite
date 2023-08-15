from flask import render_template, request, redirect, url_for, session
from auth import is_admin

def setup_admin_routes(app, users):
    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        if not session.get('logged_in'):
            return redirect(url_for('login'))

        if not is_admin(session['username']):
            return render_template('admin.html', admin=False)

        return render_template('admin.html', admin=True, users=users)

    @app.route('/admin/edit', methods=['POST'])
    def edit_user_data():
        if not session.get('logged_in'):
            return redirect(url_for('login'))

        if not is_admin(session['username']):
            return redirect(url_for('admin'))

        username = request.form['username']
        new_password = request.form['new_password']

        users[username] = new_password  # Update the password for the selected user

        return redirect(url_for('admin'))
