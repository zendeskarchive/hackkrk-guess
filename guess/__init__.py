from os import environ
from flask import Flask
from flask_heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy


AUTH_TOKEN = 'X-Auth-Token'

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///test.db')
