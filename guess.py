from flask import Flask, request, jsonify

app = Flask(__name__)

riddle = {
    'id': 1,
    'question': 'What is your quest?',
    'photo_url': 'http://f.cl.ly/items/1a3m2x1P3A0m1x3J031f/kitten.jpeg',
    'attempted_by': 7,
    'solved_by': 4,
    'points': 2,
    'solved': False,
    'created_at': '2012-06-21T18:20:12Z',
    'author': 'test_user',
}

def a_riddle(id):
    return dict(riddle, id=id)

@app.route('/user', methods=['GET', 'POST'])
def user():
    return jsonify({
        'username': 'hackkrk',
        'token': 'dead00coffee'
    })

@app.route("/riddles", methods=["GET"])
def riddles():
    return jsonify({
        'riddles': [a_riddle(n+1) for n in range(5)],
        'total': 5,
        'page': 1,
        'page_count': 1,
    })

@app.route("/riddles", methods=["POST"])
def post_riddle():
    return jsonify(riddle)

@app.route("/riddles/<id>/answer", methods=["POST"])
def answer_riddle(id):
    return jsonify({
        "id": id,
        "correct": True,
        "points": 2,
        "new_score": 10
    })

@app.route("/leaderboard")
def leaderboard():
    return jsonify({
        'users': [
            { "name": "isaac_newton", "score": "54" },
            { "name": "carl_sagan", "score": "37" },
        ],
        'count': 2,
        'page': 1,
        'page_count': 1
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)
