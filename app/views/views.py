from app import app
from app import render_template
from app.db.user import User

from flask import flash
from flask import redirect
from flask import request
from flask_login import login_required
from flask_login import login_user


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.get_verified_user(email, password)
    if user:
        login_user(user, remember=True)
        return redirect('/profile')
    flash("There was an error authenticating your user account.", "warning")
    return redirect('/login')


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')
