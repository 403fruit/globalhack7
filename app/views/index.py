from flask import Blueprint, render_template, g, current_app, url_for, redirect


app = Blueprint('index', __name__)


@app.route('/')
def index():
    return render_template('index.jinja.html')


