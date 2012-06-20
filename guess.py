import base64
import hashlib
import os
from os import environ
from flask import Flask, request, jsonify
from flask_heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import HTTPException
import wtforms
import boto
from boto.s3.key import Key

from wtforms import validators

BUCKET_NAME = 'guess'
AWS_URL_TEMPLATE = 'https://guess.s3.amazonaws.com/%s'

AUTH_TOKEN = 'X-Auth-Token'

app = Flask(__name__)
db = SQLAlchemy(app)
heroku = Heroku(app)

if not 'DATABASE_URL' in environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


class Unauthorized(HTTPException):
    pass


class UserForm(wtforms.Form):
    username = wtforms.TextField(validators=[validators.required()])
    password = wtforms.TextField(validators=[validators.required()])


class RiddleForm(wtforms.Form):
    question = wtforms.TextField(validators=[validators.required()])
    answer = wtforms.TextField(validators=[validators.required()])
    photo = wtforms.TextField(validators=[validators.required(),
                                          validators.length(max=1024 * 1024 * 5)])

class AttemptForm(wtforms.Form):
    answer = wtforms.TextField(validators=[validators.required()])

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(100), unique=True)
    password_hash = db.Column(db.Unicode(100))
    token = db.Column(db.Unicode(100), unique=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = hashlib.md5(value).hexdigest()

    def check_password(self, value):
        return self.password_hash == hashlib.md5(value).hexdigest()

    def generate_token(self):
        self.token = hashlib.md5(os.urandom(124)).hexdigest()
        return self.token

    @classmethod
    def from_token(cls, token):
        return cls.query.filter_by(token=token).first()


def authenticate():
    token = request.headers.get(AUTH_TOKEN)
    token = params().get('token', token)
    user = User.from_token(token)
    if user:
        return user
    else:
        raise HTTPException()


class Riddle(db.Model):
    __tablename__ = 'riddles'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.UnicodeText)
    answer = db.Column(db.UnicodeText)
    photo_url = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship(User, primaryjoin=(author_id==User.id))

    attempts = db.relationship("Attempt", backref="riddle")

    @property
    def author_name(self):
        return self.author.username

class Attempt(db.Model):
    __tablename__ = 'attempts'
    answer_text = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User, primaryjoin=(user_id==User.id))
    riddle_id = db.Column(db.Integer, db.ForeignKey('riddles.id'))
    riddle = db.relationship(Riddle, primaryjoin=(riddle_id==Riddle.id))
    successful = db.Column(db.Boolean(default=False))

    @property
    def answer(self):
        return self.answer_text

    @answer.setter
    def answer(self, value):
        self.successful = (value == self.riddle.answer)
        self.answer_text = value


def user_view(user):
    return {
        'username': user.username,
        'token': user.token,
    }

def riddle_view(riddle):
    return {
        'id': riddle.id,
        'question': riddle.question,
        'photo_url': riddle.photo_url,
        'author': riddle.author_name,
    }

def attempt_view(attempt):
    return {
        'answer': attempt.answer,
        'successful': attempt.successful
    }

def errors(errors, code=400):
    resp = jsonify(errors)
    resp.status_code = code
    return resp

def upload_photo(username, photo):
    data = base64.b64decode(photo)
    s3 = boto.connect_s3()
    bucket = s3.get_bucket(BUCKET_NAME)
    key = Key(bucket)
    key.content_type = 'image/jpg'
    key.key = 'photos/%s/%s.jpg' % (username, hashlib.md5(os.urandom(64)).hexdigest())
    key.set_contents_from_string(data)
    key.close()
    key.make_public()
    return AWS_URL_TEMPLATE % key.key


@app.route('/user', methods=['GET'])
def validate_user():
    form = UserForm(params())
    if form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            return jsonify(user_view(user))
        else:

            return errors({ "error": "Account doesn't exist." })
    else:
        return errors(form.errors)

@app.route('/user', methods=['POST'])
def create_user():
    try:
        form = UserForm(params())
        if form.validate():
            user = User()
            user.generate_token()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            return jsonify(user_view(user))
        else:
            return errors(form.errors)
    except IntegrityError:
        resp = jsonify({
            'username': "Username already taken",
        })
        resp.status_code = 400
        return resp


@app.route("/riddles", methods=["GET"])
def riddles():
    pass

@app.route("/riddles", methods=["POST"])
def post_riddle():
    user = authenticate()
    form = RiddleForm(params())
    if form.validate():
        photo_url = upload_photo(user.username, form.photo.data)

        riddle = Riddle()
        riddle.question = form.question.data
        riddle.answer = form.answer.data
        riddle.author = user
        riddle.photo_url = photo_url

        db.session.add(riddle)
        db.session.commit()
        return jsonify(riddle_view(riddle))
    else:
        return errors(form.errors)

@app.route("/riddles/<id>/answer", methods=["POST"])
def answer_riddle(id):
    user = authenticate()
    riddle = Riddle.query.get(id)
    form = AttemptForm(params())
    if form.validate():
        attempt = Attempt(user, riddle)
        form.populate_obj(attempt)
        db.session.add(attempt)
        db.session.commit()
        return jsonify(attempt_view(attempt))
    else:
        return errors(form.errors)

@app.route("/leaderboard")
def leaderboard():
    return jsonify({
    })

def params():
    return MultiDict(request.json)


@app.errorhandler(Unauthorized)
def unauthorized():
    return errors({'authentication': 'Please provide valid auth token'}, 401)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
