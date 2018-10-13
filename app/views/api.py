from flask import Blueprint, render_template, abort, g, current_app
from flask import jsonify, request
from flask_babel import Babel

from app.main import babel


app = Blueprint('api', __name__)


@app.route('/resources')
def get_resources():
    lang_code = request.args.get('lang_code') or 'en'
    resource_list = ['bed', 'dishes', 'stuff', 'things', 'test 4']
    return jsonify(resource_list)
