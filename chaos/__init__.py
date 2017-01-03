from api.tables import HttpStatusCodes, Base
from flask import Blueprint, current_app as app
import random

chaos = Blueprint('chaos', __name__)


@chaos.route('/', defaults={'path': '/'})
@chaos.route('/<path:path>')
def catch_all(path):
    db = app.data.driver
    Base.metadata.bind = db.engine
    db.Model = Base

    bootstrap_data = list(db.session.query(HttpStatusCodes).all())
    status_code = random.choice(bootstrap_data)
    return status_code.message + ' - ' + path, status_code.status_code
