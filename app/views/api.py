from flask import Blueprint, render_template, abort, g, current_app
from flask import jsonify, request
from flask_babel import Babel
from app.models.common import Category, Resource


from app.main import babel


app = Blueprint('api', __name__)


@app.route('/resources')
def get_resources():
    query = request.args.get('query')
    lang_code = request.args.get('lang_code') or 'en'
    resource_list = []

    categories = Category.query.filter(Category.name.like('%{}%'.format(query))).all()
    resource_list = [cat.name for cat in categories]
    return jsonify(resource_list)
