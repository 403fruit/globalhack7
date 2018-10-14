from flask import Blueprint, render_template, abort, g, current_app
from flask import jsonify, request
from flask_babel import Babel
from app.models.common import Category, Resource


from app.main import db


app = Blueprint('api', __name__)


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
