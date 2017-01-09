#!/usr/bin/env python
from api.tables import HttpStatusCodes, Base
from chaos import chaos
from dashboard import dashboard
from eve import Eve
from eve_swagger import swagger, add_documentation
from eve_sqlalchemy import SQL
from eve_sqlalchemy.decorators import registerSchema
from eve_sqlalchemy.validation import ValidatorSQL
import os
import yaml

registerSchema('codes')(HttpStatusCodes)

SETTINGS = {
    'DOMAIN': {
        'codes': HttpStatusCodes._eve_schema['codes'],
    },
    'ENFORCE_IF_MATCH': False,
    'ITEM_METHODS': ['GET', 'PATCH'],
    'RESOURCE_METHODS': ['GET'],
    'SWAGGER_INFO': {
        'title': 'Marten',
        'version': '1.0',
        'description': 'Http chaos monkey server.',
        'termsOfService': 'This will definitely break your application.',
        'contact': {
            'name': 'Gaggl team',
            'url': 'http://gaggle.io'
        },
        'license': {
            'name': 'MIT',
            'url': 'https://github.com/gaggl/marten/blob/master/LICENSE',
        }
    },
    'SQLALCHEMY_DATABASE_URI': 'sqlite://',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'URL_PREFIX': 'marten/v1',
    'X_ALLOW_CREDENTIALS': False,
    'X_DOMAINS': ['http://localhost:5000',
                  'http://editor.swagger.io'],
    'X_HEADERS': ['Content-Type', 'If-Match'],
    'XML': False,
}
app = Eve(auth=None,
          data=SQL,
          settings=SETTINGS,
          static_url_path='/marten/static',
          static_folder=os.path.join(os.environ.get('PWD'), 'static'),
          validator=ValidatorSQL)

app.register_blueprint(swagger, url_prefix='/marten')

app.register_blueprint(dashboard, url_prefix='/marten/status')

app.register_blueprint(chaos, url_prefix='')

db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base

if __name__ == '__main__':
    try:
        with open('marten.yaml', 'r') as data_file:
            bootstrap_data = yaml.load(data_file.read())
    except IOError:
        with open('example/marten.yaml', 'r') as data_file:
            bootstrap_data = yaml.load(data_file.read())
    except:
        raise
    HttpStatusCodes.bootstrap(db, bootstrap_data)

    if 'AUTO_RELOAD' in os.environ:
        reload = bool(os.environ.get('AUTO_RELOAD'))
    else:
        reload = False
    if 'DEBUG' in os.environ:
        debug = bool(os.environ.get('DEBUG'))
    else:
        debug = False
    if 'HOST' in os.environ:
        host = str(os.environ.get('HOST'))
    else:
        host = '127.0.0.1'
    if 'PORT' in os.environ:
        port = int(os.environ.get('PORT'))
    else:
        port = 5000

    app.run(
        debug=debug,
        host=host,
        port=port,
        use_reloader=reload
    )
