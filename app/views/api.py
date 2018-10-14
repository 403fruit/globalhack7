from flask import Blueprint, render_template, abort, g, current_app
from flask import jsonify, request
from flask_babel import Babel
from app.models.common import Category, Resource
from app.main import babel
from sqlalchemy import or_
import emoji
import json
from app.main import db


app = Blueprint('api', __name__)


def text_has_emoji(text):
    for char in text:
        if char in emoji.UNICODE_EMOJI:
            return True
    return False


@app.route('/resources_autosuggest')
def get_resources_autosuggestions():
    query = request.args.get('query')

    # Find all HAVE resources that match by name, and all HAVE resources that match category name
    resources = db.session.query(Resource).filter(Resource.name.like(f'%{query}%'), Resource.type == 'HAVE').all()
    categories = db.session.query(Category).filter(Category.name.like(f'%{query}%')).all()
    resources += [r for cat in categories for r in cat.resources if r.type == 'HAVE']

    # Build response as dict of {'Matching Phrase': [resources that match]}
    response = {}
    for resource in resources:
        key = f'{resource.name} ({resource.category.name})'
        response.setdefault(key, []).append(resource.serialize())
    return jsonify(response)


@app.route('/resources')
def get_resources():
    query = request.args.get('query')
    lang_code = request.args.get('lang_code') or 'en'
    resource_list = []

    if text_has_emoji(query):
        query = hex(ord(query[0]))
        with open('emoji.json') as f:
            data = json.load(f)
            emoji = next((x for x in data if x['code'].lower() == query.lower()), None)
        cat_query = Category.query.filter(or_(*[Category.name.like('%{}%'.format(keyword)) for idx, keyword in enumerate(emoji['keywords'])]))
    else:
        cat_query = Category.query.filter(Category.name.like('%{}%'.format(query)))

    categories = cat_query.all()
    resource_list = [cat.name for cat in categories]
    return jsonify(resource_list)