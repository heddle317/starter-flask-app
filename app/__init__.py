import logging
import json
import sys

from app import config

from flask import Flask
from flask import g
from flask import render_template as render_template_view

from flask.ext.compress import Compress
from flask.ext.login import current_user
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__,
            template_folder=config.TEMPLATE_FOLDER,
            static_folder=config.STATIC_FOLDER)
app.config.from_object(config)
Compress(app)
db = SQLAlchemy(app)
csrf = CsrfProtect(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = None
login_manager.init_app(app)

from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler('{}/application.log'.format(config.LOG_PATH), 'a', 1 * 1024 * 1024, 10)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
handler.setFormatter(logFormatter)

consoleHandlerOut = logging.StreamHandler(sys.stdout)
consoleHandlerOut.setFormatter(logFormatter)

consoleHandlerErr = logging.StreamHandler(sys.stderr)
consoleHandlerErr.setFormatter(logFormatter)

app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.addHandler(consoleHandlerOut)


@login_manager.user_loader
def load_user(id):
    from app.db.user import User
    user = User.get(uuid=id)
    return user


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(500)
def internal_error(exception):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def render_template(template_name, **kwargs):
    kwargs['app_base_link'] = config.APP_BASE_LINK
    kwargs['current_user'] = current_user
    return render_template_view(template_name, **kwargs)


def render_json(data, response_code):
    return json.dumps(data), response_code, {'Content-Type': 'application/json'}


from app import assets  # NOQA
from app.apis import *  # NOQA
from app.views import *  # NOQA
