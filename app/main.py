from functools import wraps

from flask import Flask, json, request
from werkzeug.exceptions import HTTPException

from settings import HOST, PORT
from communications import (
    check_auth,
    access_token,
    register,
)


app = Flask(__name__)


def is_authorized(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")
        auth_response = check_auth(authorization)
        if auth_response["code"] == 200:
            setattr(request, "user_id", auth_response["data"]["user_id"])
            return f(*args, **kwargs)
        else:
            return auth_response, auth_response["code"]
    return decorated_func


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        # "name": e.name,
        "data": {},
        "errors": [e.description],
    })
    response.content_type = "application/json"
    return response


@app.route("/access_token", methods=["POST"])
def access_token_endpoint():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    response = access_token(username, password)
    return response, response["code"]


@app.route("/register", methods=["POST"])
def register_endpoint():
    username = request.json.get("username", "")
    password = request.json.get("password", "")
    email = request.json.get("email", "")

    response = register(username, password, email)
    return response, response["code"]


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
