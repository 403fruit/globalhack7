from flask import Blueprint, render_template, abort, g, current_app
from flask import jsonify, request
from flask_babel import Babel
from app.models.common import Category, Resource
from app.main import babel
from operator import or_
import emoji
import json


app = Blueprint('api', __name__)


def text_has_emoji(text):
    for char in text:
        if char in emoji.UNICODE_EMOJI:
            return True
    return False


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
        cat_query = Category.query.filter(or_(*[Category.name.like('%{}%'.format(keyword)) for keyword in emoji['keywords']]))
    else:
        cat_query = Category.query.filter(Category.name.like('%{}%'.format(query)))

    categories = cat_query.all()
    resource_list = [cat.name for cat in categories]
    return jsonify(resource_list)
