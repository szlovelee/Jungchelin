from flask import request, redirect, jsonify

from . import bp
from app.services import resto_service, user_service
from app.utils import jwt_required
from app.utils.jwt_utils import get_user_id_from_token


def is_ajax_request():
    return request.headers.get(
        "X-Requested-With"
    ) == "XMLHttpRequest"


@bp.route("/restaurants", methods=["POST"])
@jwt_required
def add_resto():
    user_id = get_user_id_from_token()

    resto = {
        "name": request.form.get("name","").strip(),
        "category": request.form.get("category","").strip(),
        "addr": request.form.get("addr","").strip(),
        "main_menu": request.form.get("main_menu","").strip()
    }

    if (
        not resto["name"]
        or not resto["category"]
        or not resto["addr"]
    ):
        if is_ajax_request():
            return jsonify({
                "success": False,
                "code": "REQUIRED",
                "msg": "식당 이름, 분류, 주소를 입력해주세요."
            }), 400

        return redirect("/home?error=required")

    result = resto_service.add_resto(resto, user_id)

    if not result["success"]:
        if is_ajax_request():
            return jsonify({
                "success": False,
                "code": "DUPLICATE_RESTAURANT",
                "msg": "이미 등록된 식당입니다."
            }), 409

        return redirect("/home?error=duplicate")

    if is_ajax_request():
        return jsonify({
            "success": True,
            "msg": "식당이 등록되었습니다."
        }), 201

    return redirect("/home")


@bp.route("/restaurants/detail", methods=["GET"])
def get_selected_restaurant_detail():
    restaurant_id = request.args.get("restaurant_id")

    if not restaurant_id:
        return {
            "success": False,
            "msg": "식당 ID가 필요합니다."
        }, 400

    result = resto_service.get_resto_detail(restaurant_id)

    if result is None:
        return {
            "success": False,
            "msg": "식당을 찾을 수 없습니다."
        }, 404

    return result


@bp.route('/restaurants/pinned', methods=["GET"])
@jwt_required
def get_user_fav_resto():
    user_id = get_user_id_from_token()
    restaurant_id = request.args.get("restaurant_id")

    if not restaurant_id:
        return {
            "success": False,
            "msg": "식당 ID가 필요합니다."
        }, 400
    
    return user_service.get_user_fav_resto(user_id)


@bp.route('/restaurants/<resto_id>/pin', methods=["POST"])
@jwt_required
def toggle_resto_pin(resto_id):
    print("toggle pin called")
    user_id = get_user_id_from_token()

    user_service.toggle_fav_resto(user_id, resto_id)

    return redirect(
        request.referrer or '/home'
        )
