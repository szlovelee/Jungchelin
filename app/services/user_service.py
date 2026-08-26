import bcrypt

from app.db import user_db


def check_id_duplication(custom_id):
    return user_db.read_by_custom_id(
        custom_id
    ) is None


def get_user(user_id):
    return user_db.read_user(
        user_id
    )


def get_user_name(user_id):
    user = user_db.read_user(
        user_id
    )

    if user is None:
        return None

    return user.get("name")


def update_user_info(user_id, new_info):
    user = user_db.read_user(
        user_id
    )

    if user is None:
        return {
            "success": False,
            "code": "USER_NOT_FOUND",
            "msg": "사용자를 찾을 수 없습니다."
        }

    update_data = {}

    for key in [
        "name",
        "track",
        "cohort",
        "number"
    ]:
        if key in new_info and new_info[key]:
            update_data[key] = new_info[key]

    if "pw" in new_info or "pw_confirm" in new_info:
        pw = new_info.get(
            "pw",
            ""
        )

        pw_confirm = new_info.get(
            "pw_confirm",
            ""
        )

        if not pw or pw != pw_confirm:
            return {
                "success": False,
                "code": "PW_MISMATCH",
                "msg": "비밀번호가 일치하지 않습니다."
            }

        update_data["pw"] = bcrypt.hashpw(
            pw.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    if not update_data:
        return {
            "success": False,
            "code": "NO_UPDATES",
            "msg": "수정할 정보가 없습니다."
        }

    result = user_db.update_user(
        user_id,
        update_data
    )

    if result is None or result.matched_count == 0:
        return {
            "success": False,
            "code": "DATABASE_FAILED",
            "msg": "정보 수정에 실패했습니다."
        }

    return {
        "success": True
    }