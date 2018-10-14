from flask import Blueprint, render_template, g, current_app, url_for, redirect, flash, request
from flask_login import current_user
from flask_babel import gettext

from app.models.common import Category, Resource
from app.main import db


app = Blueprint('index', __name__)


@app.route('/')
@app.route('/category/<int:cat_id>')
def index(cat_id=None):
    cat_drilldown = []
    resources = []
    if cat_id:
        category = Category.query.get(cat_id)
        if not category:
            flash(gettext("Can't find the requested category"), 'danger')
        else:
            while category:
                cat_drilldown.append(category)
                category = category.parent
        resources = Resource.query.filter(Resource.category_id == cat_id).all()

    if cat_drilldown:
        cat_list = list(cat_drilldown[0].children)
    else:
        cat_list = Category.query.filter(Category.parent == None).all()

    has_requested_resource = False
    if current_user.is_authenticated():
        for resource in Resource.query.filter(Resource.user_id == current_user.id).all():
            if resource.requested and not resource.fulfilled:
                has_requested_resource = True
                break

    return render_template(
        'index.jinja.html',
        cat_drilldown=list(reversed(cat_drilldown)),
        cat_list=cat_list,
        resources=resources,
        has_requested_resource=has_requested_resource
    )


@app.route('/', methods=['POST'])
def submit():
    resource_data = request.form.get('resource_ids').split(',')
    resources = db.session.query(Resource).filter(Resource.id.in_(resource_data))
    model_resource = resources.first()

    if request.form.get('is_have') != 'false':
        # Redirect to HAVE creation (resource may or may not exist to model after)
        return redirect(
            url_for('resource.resource_create',
                    lang_code=g.lang_code or 'en',
                    name=model_resource.name if model_resource else resource_data,
                    type='HAVE',
                    cat_id=model_resource.category_id if model_resource else ''))

    if not resources.count():
        # No resources exist, create NEED resource
        flash(gettext("Sorry, we can't find that. If you give us some information about it, we will notify you if it becomes available."))
        return redirect(
            url_for('resource.resource_create',
                    lang_code=g.lang_code or 'en',
                    name=model_resource.name if model_resource else resource_data,
                    type='NEED',
                    cat_id=model_resource.category_id if model_resource else ''))
    else:
        # Resources exist, show NEEDER
        return render_template(
            'index.jinja.html',
            resources=resources
        )
