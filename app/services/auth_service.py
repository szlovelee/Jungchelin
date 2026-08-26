import re

import bcrypt

from app.db import user_db
from app.services import user_service


def login(custom_id: str, pw: str):
    user = user_db.read_by_custom_id(custom_id)

    if user is None:
        return {
            "success": False,
            "code": "ID_NOT_FOUND",
            "msg": "존재하지 않는 아이디입니다."
        }

    stored_pw = user.get("pw", "")

    if isinstance(stored_pw, str) and stored_pw.startswith("$2"):
        password_correct = bcrypt.checkpw(
            pw.encode("utf-8"),
            stored_pw.encode("utf-8")
        )
    else:
        password_correct = stored_pw == pw

    if not password_correct:
        return {
            "success": False,
            "code": "PW_WRONG",
            "msg": "비밀번호가 올바르지 않습니다."
        }

    return {
        "success": True,
        "user_id": str(user["_id"])
    }


def join_service(user):
    custom_id = user["custom_id"]
    pw = user["pw"]
    pw_confirm = user["pw_confirm"]

    if not re.fullmatch(r"[A-Za-z0-9]{6,}", custom_id):
        return {
            "success": False,
            "code": "INVALID_ID",
            "msg": "아이디는 영문과 숫자로 6자 이상 입력해주세요."
        }

    if not user_service.check_id_duplication(custom_id):
        return {
            "success": False,
            "code": "ID_DUPLICATION",
            "msg": "이미 사용 중인 아이디입니다."
        }

    if len(pw) < 9:
        return {
            "success": False,
            "code": "PW_TOO_SHORT",
            "msg": "비밀번호는 9자 이상 입력해주세요."
        }

    if pw != pw_confirm:
        return {
            "success": False,
            "code": "PW_MISMATCH",
            "msg": "비밀번호가 일치하지 않습니다."
        }

    hashed_pw = bcrypt.hashpw(
        pw.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user["pw"] = hashed_pw
    user.pop("pw_confirm", None)

    user_db.create_user(user)

    return {
        "success": True
    }