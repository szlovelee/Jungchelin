from flask import render_template, redirect, request

from . import bp
from app.services import resto_service
from app.utils import jwt_required
from app.utils.jwt_utils import get_user_id_from_token


@bp.route("/")
def index_page():
    return redirect("/login")


@bp.route("/preview")
def preview_home():
    restaurants = resto_service.load_resto_list()

    return render_template(
        "home.html",
        restaurants=restaurants,
        selected_restaurant=None,
        reviews=[]
    )


@bp.route("/home")
@jwt_required
def home_page():
    user_id = get_user_id_from_token()
    sort_key = request.args.get("sort")

    restaurants = resto_service.load_resto_list(sort_key)

    restaurant_id = request.args.get("restaurant_id")
    selected_restaurant = None
    reviews = []

    if restaurant_id:
        selected_restaurant = resto_service.get_resto_detail(restaurant_id)

    return render_template(
        "home.html",
        user_id=user_id,
        restaurants=restaurants,
        selected_restaurant=selected_restaurant,
        reviews=reviews
    )