from flask import render_template, redirect, request

from . import bp
from app.services import resto_service
from app.services import review_service
from app.services import user_service
from app.utils import jwt_required
from app.utils.jwt_utils import get_user_id_from_token


@bp.route("/")
def index_page():
    return redirect("/login")


@bp.route("/preview")
@jwt_required
def preview_home():
    user_id = get_user_id_from_token()
    sort_key = request.args.get(
        "sort",
        "star"
    )

    restaurants = resto_service.load_resto_list(user_id, sort_key)

    return render_template(
        "home.html",
        restaurants=restaurants,
        selected_restaurant=None,
        reviews=[],
        current_sort=sort_key
    )


@bp.route("/home")
@jwt_required
def home_page():
    user_id = get_user_id_from_token()
    pinned_resto = user_service.get_user_fav_resto(user_id)

    sort_key = request.args.get(
        "sort",
        "star"
    )

    restaurants = resto_service.load_resto_list(user_id, sort_key)

    restaurant_id = request.args.get(
        "restaurant_id"
    )

    selected_restaurant = None
    reviews = []

    if restaurant_id:
        selected_restaurant = (
            resto_service.get_resto_detail(
                restaurant_id
            )
        )

        if selected_restaurant:
            reviews = review_service.get_review_list(
                restaurant_id
            )

            for review in reviews:
                review["nickname"] = (
                    user_service.get_user_name(
                        str(review["user"])
                    )
                )
                review["like_status"] = user_id in review['liked']

    return render_template(
        "home.html",
        user_id=user_id,
        pinned=pinned_resto,
        restaurants=restaurants,
        selected_restaurant=selected_restaurant,
        reviews=reviews,
        current_sort=sort_key
    )