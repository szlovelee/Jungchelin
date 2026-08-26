from flask import request, redirect

from . import bp
from app.services import resto_service
from app.utils import jwt_required
from app.utils.jwt_utils import get_user_id_from_token


@bp.route("/restaurants", methods=["POST"])
@jwt_required
def add_resto():
    user_id = get_user_id_from_token()

    resto = {
        "name": request.form.get("name", "").strip(),
        "category": request.form.get("category", "").strip(),
        "addr": request.form.get("addr", "").strip(),
        "main_menu": request.form.get("main_menu", "").strip()
    }

    if not resto["name"] or not resto["category"] or not resto["addr"]:
        return redirect("/home?error=required")

    result = resto_service.add_resto(resto, user_id)

    if not result["success"]:
        return redirect("/home?error=duplicate")

    return redirect("/home")