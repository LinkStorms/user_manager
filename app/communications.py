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
