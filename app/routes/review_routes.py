from flask import request, redirect

from . import bp
from app.services import review_service
from app.utils import jwt_required
from app.utils.jwt_utils import get_user_id_from_token


@bp.route("/reviews", methods=["POST"])
@jwt_required
def add_review():
    user_id = get_user_id_from_token()

    resto_id = (
        request.form.get("resto_id")
        or request.form.get("restaurant_id")
        or ""
    ).strip()

    comment = request.form.get(
        "comment",
        ""
    ).strip()

    star_text = request.form.get(
        "star",
        ""
    ).strip()

    if not resto_id or not comment or not star_text:
        return redirect(
            f"/home?restaurant_id={resto_id}&error=review_required"
        )

    try:
        star = int(star_text)
    except ValueError:
        return redirect(
            f"/home?restaurant_id={resto_id}&error=review_star"
        )

    if star < 1 or star > 5:
        return redirect(
            f"/home?restaurant_id={resto_id}&error=review_star"
        )

    result = review_service.add_review(
        resto_id,
        user_id,
        comment,
        star
    )

    if not result["success"]:
        return redirect(
            f"/home?restaurant_id={resto_id}"
            f"&error={result['code']}"
        )

    return redirect(
        f"/home?restaurant_id={resto_id}"
    )


@bp.route("/reviews/<review_id>/like", methods=["POST"])
@jwt_required
def toggle_like(review_id):
    user_id = get_user_id_from_token()

    result = review_service.toggle_like(
        review_id,
        user_id
    )

    if not result["success"]:
        return redirect(
            "/home?error=review_not_found"
        )

    return redirect(
        f"/home?restaurant_id={result['resto_id']}"
    )


@bp.route("/reviews/<review_id>/edit", methods=["POST"])
@jwt_required
def edit_review(review_id):
    user_id = get_user_id_from_token()

    comment = request.form.get(
        "comment",
        ""
    ).strip()

    star_text = request.form.get(
        "star",
        ""
    ).strip()

    if not comment or not star_text:
        return redirect(
            "/mypage?error=review_required"
        )

    try:
        star = int(star_text)
    except ValueError:
        return redirect(
            "/mypage?error=review_star"
        )

    if star < 1 or star > 5:
        return redirect(
            "/mypage?error=review_star"
        )

    result = review_service.edit_review(
        review_id,
        user_id,
        comment,
        star
    )

    if not result["success"]:
        return redirect(
            f"/mypage?error={result['code']}"
        )

    return redirect("/mypage")


@bp.route("/reviews/<review_id>/delete", methods=["POST"])
@jwt_required
def delete_review(review_id):
    user_id = get_user_id_from_token()

    result = review_service.delete_review(
        review_id,
        user_id
    )

    if not result["success"]:
        return redirect(
            f"/mypage?error={result['code']}"
        )

    return redirect("/mypage")


@bp.route('/review/exists', methods=["GET"])
def user_already_reviewed():
  user_id = get_user_id_from_token()
  return review_service.user_reviewed(user_id)