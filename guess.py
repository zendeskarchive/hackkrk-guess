import hashlib
import os
from os import environ
from flask import Flask, request, jsonify
from flask_heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import MultiDict
import wtforms
from wtforms import validators


app = Flask(__name__)
db = SQLAlchemy(app)
heroku = Heroku(app)

if not 'DATABASE_URL' in environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


class UserForm(wtforms.Form):
    username = wtforms.TextField(validators=[validators.required()])
    password = wtforms.TextField(validators=[validators.required()])


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(100), unique=True)
    password_hash = db.Column(db.Unicode(100))
    token = db.Column(db.Unicode(100))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = hashlib.md5(value).hexdigest()

    def is_password(self, value):
        return self.password_hash == hashlib.md5(value).hexdigest()

    def generate_token(self):
        self.token = hashlib.md5(os.urandom(64)).hexdigest()
        return self.token


class Riddle(db.Model):
    __tablename__ = 'riddles'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.UnicodeText)
    answer = db.Column(db.UnicodeText)
    photo_url = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship(User, primaryjoin=(author_id==User.id))



@app.route('/user', methods=['GET'])
def validate_user():
    return jsonify({
    })

@app.route('/user', methods=['POST'])
def create_user():
    try:
        form = UserForm(MultiDict(request.json))
        if form.validate():
            user = User()
            user.generate_token()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'username': user.username,
                'token': user.token,
            })
        else:
            resp = jsonify(form.errors)
            resp.status_code = 400
            return resp
    except IntegrityError:
        resp = jsonify({
            'username': "Username already taken",
        })
        resp.status_code = 400
        return resp

@app.route("/riddles", methods=["GET"])
def riddles():
    return jsonify({
    })

@app.route("/riddles", methods=["POST"])
def post_riddle():
    return jsonify({

    })

@app.route("/riddles/<id>/answer", methods=["POST"])
def answer_riddle(id):
    return jsonify({
    })

@app.route("/leaderboard")
def leaderboard():
    return jsonify({
    })

if __name__ == '__main__':

    app.run(debug=True, port=8000)
