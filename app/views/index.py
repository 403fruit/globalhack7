from flask import Blueprint, render_template, g, current_app, url_for, redirect


app = Blueprint('index', __name__)


@app.route('/')
def index():
    if g.lang_code is None:
        return redirect(url_for('index.index', lang_code='en'))
    return render_template('index.jinja.html')


