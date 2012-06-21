from os import environ
from flask import Flask
from flask_heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry


AUTH_TOKEN = 'X-Auth-Token'

app = Flask(__name__)
db = SQLAlchemy(app)
sentry = Sentry(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///test.db')

