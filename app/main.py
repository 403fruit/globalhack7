import json
import os
import logging

from flask import Flask, g, current_app, abort

from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_babel import Babel

from app.lib.storage import file_url


logger = logging.getLogger(__name__)

# Plugin instances
bootstrap = Bootstrap()
manager = None
db = SQLAlchemy()
login_manager = LoginManager()
babel = None

# login_manager.login_view = 'user.login'
# login_manager.login_message = 'You must be logged in to access that page.'
# login_manager.login_message_category = 'danger'
# login_manager.session_protection = 'strong'


def create_app():
    global manager, babel

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
    login_manager.login_view = "login"
    babel = Babel(app)

    # jinja happy fun times
    app.jinja_env.globals.update({
        'file_url': file_url,
    })

    from app.models import common
    from app.views.index import app as index_view
    from app.views.api import app as api_view
    from app.views.user import app as user_view

    app.register_blueprint(index_view)
    app.register_blueprint(index_view, url_prefix='/<lang_code>')
    app.register_blueprint(user_view, url_prefix='/<lang_code>')
    app.register_blueprint(api_view, url_prefix='/api')

    # from app.views import view_modules
    # app.register_blueprint(index.app, url_prefix=whatever)

    @babel.localeselector
    def get_locale():
        return g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])

    @app.url_defaults
    def set_language_code(endpoint, values):
        if 'lang_code' in values or not g.get('lang_code', None):
            return
        if current_app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
            values['lang_code'] = g.lang_code

    @app.url_value_preprocessor
    def get_lang_code(endpoint, values):
        if values is not None:
            g.lang_code = values.pop('lang_code', None)

    @app.before_request
    def ensure_lang_support():
        lang_code = g.get('lang_code', None)
        if lang_code and lang_code not in current_app.config['SUPPORTED_LANGUAGES'].keys():
            return abort(404)

    return app


app = None


def get_app():
    global app
    if app is None:
        app = create_app()
    return app
