HackKRK #6 Guess App
====================

Direct your questions to Tomek ([@oinopion](http://twitter.com/oinopion)) or Tomek ([@neaf](http://twitter.com/neaf)).

Fake API instance is running at http://hackkrk-guess-static.herokuapp.com.

Live API instance is running at http://hackkrk-guess.herokuapp.com.

Always send requests with `Content-Type` header set to `application/json`.

Authentication
--------------

Auth token is required in all following requests except to `/user` endpoint
either as `X-Auth-Token` header or `token` field in request JSON.


To get auth token register new user or authenticate using `/user` endpoint.

Endpoints
---------

### POST /user

Creates new user and returns auth token.

```javascript
// Request
{
  "username": "sample_username",
  "password": "sample_password"
}

// Response
{
  "username": "sample_username",
  "token": "f136803ab9c241079ba0cc1b5d02ee77"
}
```

### GET /user

Authenticates user and returns auth token.

Takes `username` and `password` GET params.

```javascript
// Response
{
  "username": "sample_username",
  "token": "f136803ab9c241079ba0cc1b5d02ee77"
}
```

### POST /riddles

Creates new riddle.

```javascript
// Request
{
  "question": "What is it?",
  "answer": "Sample riddle",
  "photo": "…" // JPEG file encoded using Base64
}

// Response
{
  "id": 1,
  "question": "What is it?",
  "photo_url": "http://f.cl.ly/items/1a3m2x1P3A0m1x3J031f/kitten.jpeg",
  "author": "sample_username",
  "created_at": "2012-06-21T18:20:12Z"
  "attempted_by": 7, // Number of all attempts to solve the riddle
  "solved_by": 4, // Number of users who solved the riddle
  "points": 2, // Points user earns for solving the riddle
  "solved": false
}
```

### GET /riddles

Returns paginated list of all riddles.

Takes `page` and `per_page` GET params.

```javascript
// Response
{
  "total": 47
  "page": 2,
  "page_count": 5,
  "riddles": […] // Array of riddles presented as in `POST /riddles` response.
}
```

### POST /riddles/:id/answer

Registers an attempt in solvig specific riddle.

```javascript
// Request
{
  "answer": "Sample riddle",
}

// Response
{
  "id": 1
  "correct": true,
  "points": 2,
  "new_score": 7
}
```

### GET /leaderboard

Returns paginated ranking of users.

Takes `page` and `per_page` GET params.

```javascript
// Response
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
}
```
