import json
from flask import Blueprint, render_template, abort, g, current_app


app = Blueprint('index', __name__)


@app.route('/')
def index():
    return render_template('index.jinja.html')


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
