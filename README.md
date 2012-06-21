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

  # Requst:
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

  # Requst:
    {
      "username": "sample_username",
      "password": "sample_password"
    }

  # Response
    {
      "username": "sample_username",
      "token": "f136803ab9c241079ba0cc1b5d02ee77"
    }
