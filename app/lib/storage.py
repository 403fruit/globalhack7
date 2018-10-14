import os

from flask import current_app, url_for


def upload_file(uploaded_file, group, name):
    groupname = os.path.join(group, name)
    dest = os.path.join(current_app.static_folder, 'uploads', groupname)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    uploaded_file.save(dest)
    return groupname


def file_url(groupname):
    return url_for('static', filename=os.path.join('uploads', groupname))
