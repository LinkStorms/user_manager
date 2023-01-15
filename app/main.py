from functools import wraps

from flask import Flask, json, request
from werkzeug.exceptions import HTTPException
from flasgger import Swagger, swag_from

from settings import HOST, PORT
from communications import (
    check_auth,
    access_token,
    register,
    delete_token,
    add_service_token,
)


app = Flask(__name__)

Swagger(app)


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
@swag_from("flasgger_docs/access_token_endpoint.yml")
def access_token_endpoint():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    response = access_token(username, password)
    return response, response["code"]


@app.route("/delete_token", methods=["POST"])
@swag_from("flasgger_docs/delete_token_endpoint.yml")
def delete_token_endpoint():
    username = request.json.get("username", "")
    password = request.json.get("password", "")

    response = delete_token(username, password)
    return response, response["code"]


@app.route("/register", methods=["POST"])
@swag_from("flasgger_docs/register_endpoint.yml")
def register_endpoint():
    username = request.json.get("username", "")
    password = request.json.get("password", "")
    email = request.json.get("email", "")

    response = register(username, password, email)
    return response, response["code"]


@app.route("/add_service_token", methods=["POST"])
@is_authorized
def add_service_token_endpoint():
    user_id = getattr(request, "user_id", "")
    service_name = request.json.get("service_name", "")
    service_token = request.json.get("service_token", "")

    response = add_service_token(user_id, service_name, service_token)
    return response, response["code"]

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
