import logging

from flask import Flask
from flask_migrate import Migrate
from flask_redoc import Redoc
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(
    filename='record.log',
    level=logging.ERROR,
    format='%(levelname)s %(asctime)s : %(message)s'
)

app = Flask(__name__)
redoc = Redoc(app, 'yacut.yaml')

app.config.from_pyfile('settings.py', silent=False)
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from yacut import api_views, error_handlers, views
