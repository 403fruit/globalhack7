import json

from flask import Blueprint, render_template, abort, g, current_app, redirect, url_for, flash
from flask_babel import Babel
from flask_login import login_user, logout_user, current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from flask.ext.babel import gettext, lazy_gettext

from app.main import babel
from app.models.common import User

LABELS = {
    "username": lazy_gettext("Username"),
    "password": lazy_gettext("Password"),
    "remember_me": lazy_gettext("Remember Me"),
    "submit": lazy_gettext("Sign In"),
}


class LoginForm(Form):
    username = StringField(LABELS['username'], validators=[DataRequired()])
    password = PasswordField(LABELS['password'], validators=[DataRequired()])
    remember_me = BooleanField(LABELS['remember_me'])
    submit = SubmitField(LABELS['submit'])

app = Blueprint('user', __name__)

@app.route('/login/', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated():
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.jinja.html', title=gettext('Sign In'), form=form)

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
