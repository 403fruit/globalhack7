from flask import Blueprint, url_for, redirect, render_template, flash, g
from flask_login import login_required

from app.models.common import Resource
from flask import Blueprint, render_template, g, current_app, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from wtforms.widgets import TextArea

from app.main import db
from app.models.common import User, Category, PRIMARY_ROLE, USER_RESOURCE_TYPES
from app.lib.constants import *


app = Blueprint('resource', __name__)


class ResourceForm(Form):
    name = StringField(LABELS['name'])
    category = SelectField(LABELS['category'])
    quantity_available = StringField(LABELS['quantity'])
    description = StringField(LABELS['bio'], widget=TextArea())
    type = HiddenField(LABELS['type'])
    picture = FileField(LABELS["picture"], description=HELP["picture"])
    submit = SubmitField(LABELS['submit_create'])


@login_required
@app.route('/<id>', methods=['GET', 'POST'])
def detail_view(id=None):
    if id == 'new':
        return 'Not Implemented Yet'
    resource = Resource.query.get(id)
    if not resource:
        flash('No resource found.', 'warning')
        return redirect(url_for('index.index', lang_code=g.lang_code))
    return render_template('resource_detail.jinja.html', resource=resource)


@app.route('/create', methods=['GET', 'POST'])
def resource_create():
    if not current_user.is_authenticated():
        flash(ERROR_MESSAGES['not_logged_in'], "warning")
        return redirect(url_for('index.index'))
    form = ResourceForm()
    form.category.choices = [(cat.id, cat.name) for cat in Category.query.all() if cat.parent]
    if request.args.get('cat_id'):
        default_cat = Category.query.get(int(request.args['cat_id']))
        form.category.data = default_cat.id
    if request.args.get('name'):
        form.name.data = request.args['name']
    if request.args.get('resource_type'):
        form.type.data = request.args['resource_type']

    form.type.data = request.args.get('type')

    if form.validate_on_submit():
        new_resource = Resource(
            name=form.name.data,
            category_id=form.category.data,
            quantity_available=form.quantity_available.data,
            description=form.description.data,
            picture=form.picture.data,
            fulfilled=False,
            quantity_needed=0,
            type=form.type.data,
            user_id=current_user.id
        )
        db.session.add(new_resource)
        db.session.commit()
        flash(GENERAL_MESSAGES['resource_save_success'], "success")
        return redirect(url_for('index.index'))
    return render_template('resource_editor.jinja.html', name=request.args.get('name'), form=form)
