Guess
=====

Fake API instance is running at http://hackkrk-guess-static.herokuapp.com.

Authentication
--------------

Auth token is required in all following requests except to `/user` endpoint
either as `X-Auth-Token` header or `token` field in request JSON.


To get auth token register new user or authenticate using `/user` endpoint.

Endpoints
---------

### POST /user

Creates new user and returns auth token.

    # Request
    {
      "username": "sample_username",
      "password": "sample_password"
    }

    # Response
    {
      "username": "sample_username",
      "token": "f136803ab9c241079ba0cc1b5d02ee77"
    }

### GET /user

Authenticates user and returns auth token.

    # Request
    {
      "username": "sample_username",
      "password": "sample_password"
    }

    # Response
    {
      "username": "sample_username",
      "token": "f136803ab9c241079ba0cc1b5d02ee77"
    }

### POST /riddles

Creates new riddle.

    # Request
    {
       "question": "What is it?",
       "answer": "Sample riddle",
       "photo": "…" # JPEG file encoded using Base64
    }

    # Response
    {
      "id": 1,
      "question": "What is it?",
      "photo_url": "http://f.cl.ly/items/1a3m2x1P3A0m1x3J031f/kitten.jpeg",
      "author": "sample_username",
      "created_at": "2012-06-21T18:20:12Z"
      "attempted_by": 7, # Number of all attempts to solve the riddle
      "solved_by": 4, # Number of users who solved the riddle
      "points": 2,
      "solved": false
    }

### GET /riddles

Returns paginated list of all riddles.

    # Request
    {
      "page": 2,
      "per_page": 10
    }

    # Response
    {
      "total": 47
      "page": 2,
      "page_count": 5,
      "riddles": […] # Array of riddles presented as in `POST /riddles` response.
    }

### POST /riddles/:id/answer

Registers an attempt in solvig specific riddle.

    # Request
    {
      "answer": "Sample riddle",
    }

    # Response
    {
      "id": 1
      "correct": true,
      "points": 2,
      "new_score": 7
    }

### GET /leaderboard

Returns paginated ranking of users.

    # Request
    {
      "page": 2,
      "per_page": 10
    }

    # Response
    {
      "total": 47
      "page": 2,
      "page_count": 5,
      "users": [
        {
          "username": "sample_user",
          "score": 274
        },
        {
          "username": "other_user",
          "score": 139
        },
        { … }
      ]
