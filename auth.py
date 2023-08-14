from flask import session

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            user = User(username, users[username]['password_hash'])
            if user.check_password(password):
                login_user(user)
                session['logged_in'] = True  # Set session variable
                return redirect(url_for('main.index'))
            else:
                flash('Incorrect password', 'error')
        else:
            flash('User not found', 'error')

    return render_template('login.html')
