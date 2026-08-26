from flask import render_template, redirect

from . import bp
from app.services import resto_service
from app.utils import jwt_required
from app.utils.jwt_utils import get_user_id_from_token


# 처음 접속하면 로그인 화면으로 이동
@bp.route("/")
def index_page():
    return redirect("/login")


# 로그인 없이 홈 화면 디자인만 확인하는 임시 주소
@bp.route("/preview")
def preview_home():
    return render_template(
        "home.html",
        restaurants=[],
        selected_restaurant=None,
        reviews=[]
    )


# 실제 홈 화면
@bp.route("/home")
@jwt_required
def home_page():
    user_id = get_user_id_from_token()
    restaurants = resto_service.load_resto_list();

    return render_template(
        "home.html",
        user_id=user_id,
        restaurants=[],
        selected_restaurant=None,
        reviews=[]
    )