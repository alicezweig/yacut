from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('settings.py', silent=False)
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from yacut import views, api_views
