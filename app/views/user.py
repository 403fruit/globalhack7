from flask import Blueprint, render_template, g, current_app, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from flask_babel import gettext, lazy_gettext
from wtforms.widgets import TextArea

from app.main import db
from app.models.common import User, IMMIGRATION_STATUS, PRIMARY_ROLE
from app.models.constants import COUNTRY_CODES


LABELS = {
    "username": lazy_gettext("Username"),
    "password": lazy_gettext("Password"),
    "repeat_password": lazy_gettext("Repeat Password"),
    "remember_me": lazy_gettext("Remember Me"),
    "submit_sign_in": lazy_gettext("Sign In"),
    "submit": lazy_gettext("Submit"),
    "submit_register": lazy_gettext("Register"),
    "email": lazy_gettext("Email"),
    "register": lazy_gettext("Register"),
    "name": lazy_gettext("Name"),
    "phone": lazy_gettext("Phone Number"),
    "bio": lazy_gettext("Bio"),
    "immigration_status": lazy_gettext("Immigration Status"),
    "primary_role": lazy_gettext("Primary Role"),
    "language": lazy_gettext("Language"),
    "country": lazy_gettext("Country"),
    "picture": lazy_gettext("Picture")
}
HELP = {
    "picture": lazy_gettext("Upload a picture of yourself to help others get to know you"),
}


class SUPPORTEDLANGUAGES(object):
    def __iter__(self):
        for key, value in current_app.config.get("SUPPORTED_LANGUAGES", {}).items():
            yield (key, value)


ERROR_MESSAGES = {
    "different_username": lazy_gettext("Please select a different username."),
    "different_email": lazy_gettext("Please select a different email address"),
    "invalid_credentials": lazy_gettext("Invalid username or password.")
}

GENERAL_MESSAGES = {
    "registration_success": lazy_gettext("You have successfully registered."),
    "login_success": lazy_gettext("You have successfully logged in."),
    "logout_success": lazy_gettext("You have successfully logged out.")
}


class LoginForm(Form):
    username = StringField(LABELS['username'], validators=[DataRequired()])
    password = PasswordField(LABELS['password'], validators=[DataRequired()])
    remember_me = BooleanField(LABELS['remember_me'])
    submit = SubmitField(LABELS['submit'])


class ProfileForm(Form):
    name = StringField(LABELS['name'])
    username = StringField(LABELS['username'], validators=[DataRequired()])
    email = StringField(LABELS['email'], validators=[DataRequired(), Email()])
    bio = StringField(LABELS['bio'], widget=TextArea())
    phone = StringField(LABELS["phone"])
    language = SelectField(LABELS["language"], choices=SUPPORTEDLANGUAGES())
    country = SelectField(LABELS["country"], choices=COUNTRY_CODES)
    picture = FileField(LABELS["picture"], description=HELP["picture"])
    submit = SubmitField(LABELS['submit'])


class RegistrationForm(Form):
    name = StringField(LABELS['name'])
    email = StringField(LABELS['email'], validators=[DataRequired(), Email()])
    username = StringField(LABELS['username'], validators=[DataRequired()])
    password = PasswordField(LABELS['password'], validators=[DataRequired()])
    password2 = PasswordField(
        LABELS['repeat_password'], validators=[DataRequired(), EqualTo('password')])
    bio = StringField(LABELS['bio'], widget=TextArea())
    phone = StringField(LABELS["phone"])
    language = SelectField(LABELS["language"], choices=[])
    country = SelectField(LABELS["country"], choices=COUNTRY_CODES)
    picture = FileField(LABELS["picture"], description=HELP["picture"])
    immigration_status = SelectField(LABELS["immigration_status"], choices=IMMIGRATION_STATUS)
    primary_role = SelectField(LABELS["primary_role"], choices=PRIMARY_ROLE)
    submit = SubmitField(LABELS['submit_register'])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(ERROR_MESSAGES['different_username'])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(ERROR_MESSAGES['different_email'])


app = Blueprint('user', __name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(ERROR_MESSAGES['invalid_credentials'], "warning")
            return redirect(url_for('user.login', lang_code=g.lang_code))
        login_user(user, remember=form.remember_me.data)
        flash(GENERAL_MESSAGES['login_success'], "success")
        return redirect(url_for('index.index', lang_code=user.language.lower()))
    return render_template('login.jinja.html', title=gettext('Sign In'), form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    form.language.choices = [[k, v] for k, v in current_app.config.get("SUPPORTED_LANGUAGES", {}).items()]
    if form.validate_on_submit():
        user = User(
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
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        flash(GENERAL_MESSAGES['registration_success'], "success")
        return redirect(url_for('index.index'))
    else :
        if form.language.data == "None":
            form.language.data = g.lang_code
    return render_template('register.jinja.html', title=gettext('Register'), form=form)


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def view_profile(id=None):
    user = User.query.get(id)
    if not user:
        flash(gettext('A user with that ID does not exist'), 'error')
        return redirect(url_for('index.index', lang_code=g.lang_code if g.lang_code else 'en'))

    return render_template('view_profile.jinja.html', user=user)


@app.route('/profile/edit/<int:id>', methods=['GET', 'POST'])
def edit_profile(id=None):
    user = User.query.get(id)
    if not user:
        flash(gettext('A user with that ID does not exist'), 'error')
        return redirect(url_for('index.index', lang_code=g.lang_code if g.lang_code else 'en'))
    if current_user != user:
        flash(gettext("You do not have permission to access this profile."), 'danger')
        flash(gettext('A user with that ID does not exist'), 'error')
    form = ProfileForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash(gettext('Your account has been successfully saved!'), 'success')
        return redirect(url_for('index.index', lang_code=(user.language or 'en')))

    return render_template('edit_profile.jinja.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(GENERAL_MESSAGES['logout_success'])
    return redirect(url_for('index.index'))
