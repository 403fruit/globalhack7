from flask import Blueprint, url_for, redirect, render_template, flash, g
from flask_login import login_required

from app.models.common import Resource

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
