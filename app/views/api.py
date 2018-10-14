from flask import Blueprint, render_template, abort, g, current_app
from flask import jsonify, request
from flask.ext.babel import gettext
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


@app.route('/search-resources')
def search_resources():
    query = request.args.get('query')
    g.lang_code = request.args.get('lang_code') or 'en'
    resource_list = []

    if text_has_emoji(query):
        query = hex(ord(query[0]))
        with open('emoji.json') as f:
            data = json.load(f)
            emoji = next((x for x in data if x['code'].lower() == query.lower()), None)
        cat_query = Category.query.filter(or_(*[Category.name.like(f'%{keyword}%') for keyword in emoji['keywords']]))
        res_query = db.session.query(Resource).filter(Resource.type == 'HAVE', or_(*[Resource.name.like(f'%{keyword}%') for keyword in emoji['keywords']]))
    else:
        cat_query = Category.query.filter(Category.name.like(f'%{query}%'))
        res_query = db.session.query(Resource).filter(Resource.name.like(f'%{query}%'))

    categories = cat_query.all()
    resources = res_query.all()

    # Build response as dict of {'Matching Phrase': [resources that match]}
    response = {}
    for resource in set(resources + [r for cat in categories for r in cat.resources]):
        key = '{} ({})'.format(resource.name, gettext(resource.category.name))
        response.setdefault(key, []).append({'category_id': resource.category.id, 'resource_id': resource.id})
    return jsonify(response)

