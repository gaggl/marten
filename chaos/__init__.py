from flask import Blueprint
import random

chaos = Blueprint('chaos', __name__)


@chaos.route('/', defaults={'path': '/'})
@chaos.route('/<path:path>')
def catch_all(path):
    bootstrap_data = [
        ('ok', 200, 25),
        ('moved', 300, 25),
        ('your fault', 400, 25),
        ('my fault', 500, 25),
    ]
    status_code = random.choice(bootstrap_data)
    return status_code[0] + ' - ' + path, status_code[1]
