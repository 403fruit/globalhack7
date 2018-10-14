from flask import Blueprint, url_for, redirect, render_template, flash, g
from flask_login import login_required

from app.models.common import Resource
from flask import Blueprint, render_template, g, current_app, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from wtforms.widgets import TextArea

from app.main import db
from app.models.common import User, IMMIGRATION_STATUS, PRIMARY_ROLE
from app.models.constants import COUNTRY_CODES
from app.lib.constants import *


app = Blueprint('resource', __name__)


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


class ResourceForm(Form):
    name = StringField(LABELS['name'])
    email = StringField(LABELS['email'], validators=[DataRequired(), Email()])
    assocation = StringField(LABELS['association'])
    username = StringField(LABELS['username'], validators=[DataRequired()])
    password = PasswordField(LABELS['password'], validators=[DataRequired()])
    bio = StringField(LABELS['bio'], widget=TextArea())
    phone = StringField(LABELS["phone"])
    language = SelectField(LABELS["language"], choices=[(k, v) for k,v in LANGUAGE_CHOICES.items()])
    country = SelectField(LABELS["country"], choices=COUNTRY_CODES)
    picture = FileField(LABELS["picture"], description=HELP["picture"])
    immigration_status = SelectField(LABELS["immigration_status"], choices=IMMIGRATION_STATUS)
    primary_role = SelectField(LABELS["primary_role"], choices=PRIMARY_ROLE)
    submit = SubmitField(LABELS['submit_register'])


@app.route('/create', methods=['GET'])
def resource_create():
    if current_user.is_authenticated():
        return redirect(url_for('index.index'))
    form = ResourceForm()

    if form.validate_on_submit():
        new_resource = ResourceForm(
            username=form.username.data,
            email=form.email.data,
            name=form.name.data,
            phone=form.phone.data,
            bio=form.bio.data,
            immigration_status=form.immigration_status.data,
            primary_role=form.primary_role.data,
            language=form.language.data,
            country=form.country.data,
        )
        db.session.add(new_resource)
        db.session.commit()
        flash(GENERAL_MESSAGES['registration_success'], "success")
        return redirect(url_for('index.index'))
    return render_template('register.jinja.html', name=request.args.get('name'), cat_id=request.args.get('cat_id'), form=form)
