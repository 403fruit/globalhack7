import json
import os
import logging

from flask import Flask

from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


logger = logging.getLogger(__name__)

# Plugin instances
bootstrap = Bootstrap()
manager = None
db = SQLAlchemy()
login_manager = LoginManager()

# login_manager.login_view = 'user.login'
# login_manager.login_message = 'You must be logged in to access that page.'
# login_manager.login_message_category = 'danger'
# login_manager.session_protection = 'strong'


def create_app():
    global manager

    app = Flask(__name__, static_url_path='/static')
    app._static_folder = os.path.join(os.path.dirname(__file__), 'static')

    with open('config.json', 'r') as fp:
        app.config.update(json.load(fp))

    # # Stick a logger into the app object, not sure why
    # app._logger = logging.getLogger('app')

    # Plugin initialization
    bootstrap.init_app(app)
    manager = Manager(app)
    db.init_app(app)
    login_manager.init_app(app)


    from flask import Blueprint, render_template
    index_bp = Blueprint('index', __name__)
    @index_bp.route('/')
    def index():
        return render_template('index.jinja.html')
    app.register_blueprint(index_bp)

    # from app.views import view_modules
    # app.register_blueprint(index.app, url_prefix=whatever)

    return app


app = None
def get_app():
    global app
    if app is None:
        app = create_app()
    return app
