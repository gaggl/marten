from api.tables import HttpStatusCodes, Base
from flask import Blueprint, current_app as app
import json
import numpy

chaos = Blueprint('chaos', __name__)


@chaos.route('/', defaults={'path': '/'})
@chaos.route('/<path:path>')
def catch_all(path):
    db = app.data.driver
    Base.metadata.bind = db.engine
    db.Model = Base

    dataset = db.session.query(HttpStatusCodes).all()
    probabilities = list()
    for element in dataset:
        probabilities.append(element.probability)

    status_code = numpy.random.choice(dataset, p=probabilities)
    db.session.query(HttpStatusCodes) \
              .filter(HttpStatusCodes._id == status_code._id)\
              .update({'count': status_code.count+1})
    db.session.commit()

    payload = json.loads(status_code.payload)
    body = payload['body']
    if 'headers' in payload.keys():
        headers = payload['headers']
    else:
        headers = {}
    return body, status_code.status_code, headers
