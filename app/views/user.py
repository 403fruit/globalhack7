import json

from flask import Blueprint, render_template, abort, g, current_app, redirect, url_for, flash, request
from flask_babel import Babel
from flask_login import login_user, logout_user, current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from flask_babel import gettext, lazy_gettext

from app.main import babel, db
from app.models.common import User, IMMIGRATION_STATUS, PRIMARY_ROLE


LABELS = {
    "username": lazy_gettext("Username"),
    "password": lazy_gettext("Password"),
    "repeat_password": lazy_gettext("Repeat Password"),
    "remember_me": lazy_gettext("Remember Me"),
    "submit": lazy_gettext("Sign In"),
    "email": lazy_gettext("Email"),
    "register": lazy_gettext("Register"),
    "name": lazy_gettext("Name"),
    "phone": lazy_gettext("Phone Number"),
    "bio": lazy_gettext("Bio"),
    "immigration_status": lazy_gettext("Immigration Status"),
    "primary_roll": lazy_gettext("Primary Role"),
    "language": lazy_gettext("Language"),
    "country": lazy_gettext("Country"),
}

ERROR_MESSAGES = {
    "different_username": lazy_gettext("Please select a different username."),
    "different_email": lazy_gettext("Please select a different email address"),
    "invalid_credentials": lazy_gettext("Invalid username or password.")
}

GENERAL_MESSAGES = {
    "registration_success": lazy_gettext("You have successfully registered."),
}


class LoginForm(Form):
    username = StringField(LABELS['username'], validators=[DataRequired()])
    password = PasswordField(LABELS['password'], validators=[DataRequired()])
    remember_me = BooleanField(LABELS['remember_me'])
    submit = SubmitField(LABELS['submit'])


class RegistrationForm(Form):
    name = StringField(LABELS['name'])
    email = StringField(LABELS['email'], validators=[DataRequired(), Email()])
    username = StringField(LABELS['username'], validators=[DataRequired()])
    password = PasswordField(LABELS['password'], validators=[DataRequired()])
    password2 = PasswordField(
        LABELS['repeat_password'], validators=[DataRequired(), EqualTo('password')])
    immigration_status = SelectField(LABELS["immigration_status"], choices=IMMIGRATION_STATUS)
    primary_role = SelectField(LABELS["primary_roll"], choices=PRIMARY_ROLE)
    bio = StringField(LABELS['bio'])
    phone = StringField(LABELS["phone"])
    language = StringField(LABELS["language"])
    country = StringField(LABELS["country"])
    submit = SubmitField(LABELS['submit'])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(ERROR_MESSAGES['different_username'])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(ERROR_MESSAGES['different_email'])


app = Blueprint('user', __name__)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(ERROR_MESSAGES['invalid_credentials'])
            return redirect(url_for('user.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index.index'))
    return render_template('login.jinja.html', title=gettext('Sign In'), form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            name=form.name.data,
            phone=form.phone.data,
            bio = form.bio.data,
            immigration_status=form.immigration_status.data,
            primary_role=form.primary_role.data,
            language=form.language.data,
            country=form.country.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(GENERAL_MESSAGES['registration_success'])
        return redirect(url_for('user.login'))
    return render_template('register.jinja.html', title=gettext('Register'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


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
