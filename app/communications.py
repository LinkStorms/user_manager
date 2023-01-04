import requests

from utilities import get_user_handler_url


def check_auth(authorization, user_handler_url=get_user_handler_url()):
    """
    Check if the user is authorized to access the API.
    """
    access_token = authorization.replace("Bearer ", "")

    url = f"{user_handler_url}/check_token"
    payload = {"access_token": access_token}
    response = requests.post(url, json=payload)
    return response.json()


def access_token(username, password, user_handler_url=get_user_handler_url()):
    """
    Get an access token for a user.
    """
    url = f"{user_handler_url}/access_token"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    return response.json()


def register(username, password, email, user_handler_url=get_user_handler_url()):
    """
    Register a new user.
    """
    url = f"{user_handler_url}/register"
    payload = {"username": username, "password": password, "email": email}
    response = requests.post(url, json=payload)
    return response.json()


def delete_token(username, password, user_handler_url=get_user_handler_url()):
    """
    Delete a user's access token.
    """
    url = f"{user_handler_url}/delete_token"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    return response.json()
