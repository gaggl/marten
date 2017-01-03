#!/usr/bin/env python
from api.tables import HttpStatusCodes
from chaos import chaos
from dashboard import dashboard
from eve import Eve
from eve_docs import eve_docs
from eve_sqlalchemy import SQL
from eve_sqlalchemy.decorators import registerSchema
from eve_sqlalchemy.validation import ValidatorSQL
from flask.ext.bootstrap import Bootstrap
import os

registerSchema('codes')(HttpStatusCodes)

SETTINGS = {
    'API_NAME': 'Marten',
    'DOMAIN': {
        'codes': HttpStatusCodes._eve_schema['codes'],
    },
    'SQLALCHEMY_DATABASE_URI': 'sqlite://',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'URL_PREFIX': 'api',
    'XML': False,
}
app = Eve(auth=None,
          data=SQL,
          settings=SETTINGS,
          static_url_path='/static',
          static_folder=os.path.join(os.environ.get('PWD'), 'static'),
          validator=ValidatorSQL)

Bootstrap(app)
app.register_blueprint(eve_docs, url_prefix='/docs')

app.register_blueprint(dashboard, url_prefix='/status')

app.register_blueprint(chaos, url_prefix='')

if __name__ == '__main__':
    bootstrap_data = [
        ('ok', 200, 25),
        ('moved', 300, 25),
        ('your fault', 400, 25),
        ('my fault', 500, 25),
    ]
    HttpStatusCodes.bootstrap(app, bootstrap_data)

    if 'AUTO_RELOAD' in os.environ:
        reload = bool(os.environ.get('AUTO_RELOAD'))
    else:
        reload = False
    if 'DEBUG' in os.environ:
        debug = bool(os.environ.get('DEBUG'))
    else:
        debug = False
    if 'PORT' in os.environ:
        port = int(os.environ.get('PORT'))
    else:
        port = 5000
    if 'HOST' in os.environ:
        host = str(os.environ.get('HOST'))
    else:
        host = '127.0.0.1'

    app.run(
        debug=debug,
        host=host,
        port=port,
        use_reloader=reload
    )
