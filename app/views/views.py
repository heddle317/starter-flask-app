from app import app
from app import render_template

from flask_login import login_required


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')
