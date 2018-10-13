from flask import Blueprint, render_template, g, current_app, url_for, redirect

from app.models.common import Category


app = Blueprint('index', __name__)


@app.route('/')
@app.route('/category/<int:cat_id>')
def index(cat_id=None):
    cat_drilldown = []
    if cat_id:
        category = Category.query.get(cat_id)
        if not category:
            flash(_("Can't find the requested category"), 'danger')
        else:
            while category:
                cat_drilldown.append(category)
                category = category.parent

    if cat_drilldown:
        cat_list = list(cat_drilldown[0].children)
    else:
        cat_list = Category.query.filter(Category.parent == None).all()

    return render_template(
        'index.jinja.html',
        cat_drilldown=list(reversed(cat_drilldown)),
        cat_list=cat_list,
    )


