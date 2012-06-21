from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import HTTPException
from flask import request, jsonify

from guess import app, db, AUTH_TOKEN
from guess.forms import UserForm, AttemptForm, RiddleForm
from guess.models import User, Attempt, Riddle
from guess.utils import upload_photo
from guess.views import attempt_view, riddle_view, user_view


class Unauthorized(HTTPException):
    code = 401


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
    user = authenticate()
    riddles = Riddle.query.all()


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


@app.errorhandler(401)
def unauthorized(e):
    return errors({'authentication': 'Please provide valid auth token'}, 401)


def authenticate():
    token = request.headers.get(AUTH_TOKEN)
    token = params().get('token', token)
    user = User.from_token(token)
    if user:
        return user
    else:
        raise Unauthorized()

def errors(errors, code=400):
    resp = jsonify(errors)
    resp.status_code = code
    return resp
