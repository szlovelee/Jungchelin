import bcrypt

from app.db import user_db
from app.db import track_db


def check_id_duplication(custom_id: str):
    return user_db.read_by_custom_id(custom_id) is None


def get_track_types():
    return track_db.read_active_tracks()


def get_user_name(user_id: str):
    user = user_db.read_user(user_id)

    if user is None:
        return None

    return user.get("name")


def update_user_info(user_id: str, new_info):
    user = user_db.read_user(user_id)

    if user is None:
        return {
            "success": False,
            "code": "USER_NOT_FOUND",
            "msg": "해당 사용자를 찾을 수 없습니다."
        }

    if "pw" in new_info:
        if new_info.get("pw") != new_info.get("pw_confirm"):
            return {
                "success": False,
                "code": "PW_MISMATCH",
                "msg": "비밀번호가 일치하지 않습니다."
            }

        new_info["pw"] = bcrypt.hashpw(
            new_info["pw"].encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        new_info.pop("pw_confirm", None)

    allowed_fields = {
        "name",
        "track",
        "cohort",
        "number",
        "pw"
    }

    update_data = {
        key: value
        for key, value in new_info.items()
        if key in allowed_fields
    }

    if not update_data:
        return {
            "success": False,
            "code": "NO_UPDATES",
            "msg": "수정할 정보가 없습니다."
        }

    result = user_db.update_user(user_id, update_data)

    if result.matched_count == 0:
        return {
            "success": False,
            "code": "DATABASE_FAILED",
            "msg": "정보 수정에 실패했습니다."
        }

    return {
        "success": True
    }