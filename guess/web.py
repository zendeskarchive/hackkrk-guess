from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
from werkzeug.datastructures import MultiDict
from werkzeug.exceptions import HTTPException
from flask import request, jsonify

from guess import app, db, AUTH_TOKEN
from guess.forms import UserForm, AttemptForm, RiddleForm, PageForm
from guess.models import User, Attempt, Riddle
from guess.utils import upload_photo, Pager
from guess.views import attempt_view, riddle_view, user_view, \
    riddles_listing_view, leaderboard_view


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
    total = Riddle.query.count()
    form = PageForm(params())
    if not form.validate():
        return errors(form.errors)
    pager = Pager(total=total, **form.data)
    riddles_map = {}
    riddles = Riddle.query.order_by(Riddle.created_at).slice(*pager.slice).all()
    for riddle in riddles:
        riddles_map[riddle.id] = riddle
    for (id, ) in db.session.query(Attempt.riddle_id).filter_by(successful=True).filter_by(user_id=user.id).all():
        riddles_map[id].solved = True
    for id, attempted_by in db.session.query(Attempt.riddle_id, func.count(Attempt.riddle_id)).group_by(Attempt.riddle_id).all():
        riddles_map[id].attempted_by = attempted_by
    for id, solved_by in db.session.query(Attempt.riddle_id, func.count(Attempt.riddle_id)).group_by(Attempt.riddle_id).filter_by(successful=True).all():
        riddles_map[id].solved_by = solved_by
    return jsonify(riddles_listing_view(pager, riddles))



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
    user = authenticate()
    form = PageForm(params())
    if not form.validate():
        return errors(form.errors)
    total = User.query.count()
    pager = Pager(total=total, **form.data)
    users = User.query.order_by(User.username).slice(*pager.slice)
    user_map = {}
    for user in users:
        user_map[user.id] = user
    for user_id, count in db.session.query(Attempt.user_id, db.func.count(Attempt.user_id)).group_by(Attempt.user_id).filter_by(successful=True).all():
        if user_id in user_map:
            user_map[user_id].score = count
    return jsonify(leaderboard_view(pager, users))

def params():
    if request.method == 'GET':
        return MultiDict(request.args)
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
