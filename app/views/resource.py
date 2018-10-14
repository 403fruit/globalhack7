import json
from flask import Blueprint, render_template, g, current_app, url_for, redirect, flash, request

from app.models.common import Category, Resource
from app.main import db


app = Blueprint('resource', __name__)


@app.route('/create')
def resource_create():
    return json.dumps(request.args)
