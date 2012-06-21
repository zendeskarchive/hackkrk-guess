import os
import hashlib
from guess import db



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


class Riddle(db.Model):
    __tablename__ = 'riddles'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.UnicodeText)
    answer = db.Column(db.UnicodeText)
    photo_url = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship(User, primaryjoin=(author_id==User.id))

    attempts = db.relationship('Attempt', backref='riddle')

    @property
    def author_name(self):
        return self.author.username

    @classmethod
    def for_listing(cls, user):
        q = cls.query.options(db.joinedload(Riddle.attempts))
        return q.filter(Attempt.user_id==user.id)

class Attempt(db.Model):
    __tablename__ = 'attempts'
    id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.UnicodeText)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(User, primaryjoin=(user_id==User.id))
    riddle_id = db.Column(db.Integer, db.ForeignKey('riddles.id'))
    successful = db.Column(db.Boolean, default=False)

    def __init__(self, user, riddle):
        self.user = user
        self.riddle = riddle

    @property
    def answer(self):
        return self.answer_text

    @answer.setter
    def answer(self, value):
        self.successful = (value == self.riddle.answer)
        self.answer_text = value
