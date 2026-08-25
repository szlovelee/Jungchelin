from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app, request


def create_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }

    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )


def get_user_id_from_token():
    token = request.cookies.get("access_token")

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"]
        )

        return payload["user_id"]

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None