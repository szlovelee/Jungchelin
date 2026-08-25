from functools import wraps

from flask import Blueprint, redirect

from .jwt_utils import get_user_id_from_token


bp = Blueprint("utils", __name__)


def jwt_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user_id = get_user_id_from_token()

        if user_id is None:
            return redirect("/login")

        return function(*args, **kwargs)

    return wrapper