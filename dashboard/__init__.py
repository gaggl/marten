from flask import Blueprint, current_app as app, send_from_directory

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
def send_dashboard():
    return send_from_directory(app.static_folder, 'index.html')
