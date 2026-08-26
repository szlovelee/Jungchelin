import bcrypt

from bson.objectid import ObjectId
from app.db import user_db


def check_id_duplication(custom_id:str):
    return user_db.read_by_custom_id(custom_id) is None


def get_user(id:str):
    return user_db.read_user(id)


def get_user_name(id:str):
    user = user_db.read_user(id)

    if user is None:
        return None

    return user["name"]

def get_user_fav_resto(id):
    user = user_db.read_user(id)

    if user is None:
        return None

    if "fav_resto" not in user :
      return []

    return user["fav_resto"]
    

def update_user_info(id, new_info):
    user = user_db.read_user(id)

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
        pw = new_info.get("pw","")

        pw_confirm = new_info.get("pw_confirm","")

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

    result = user_db.update_user(id, update_data)

    if result is None or result.matched_count == 0:
        return {
            "success": False,
            "code": "DATABASE_FAILED",
            "msg": "정보 수정에 실패했습니다."
        }

    return {
        "success": True
    }

def toggle_fav_resto(id:str, resto_id:str):

    pin = False
    
    if ObjectId(resto_id) in get_user_fav_resto(id):
        user_db.remove_favorite_resto(id, resto_id)
    else:
        user_db.add_favorite_resto(id, resto_id)
        pin = True

    return pin