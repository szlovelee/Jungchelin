from flask import render_template, request, redirect

from . import bp
from app import constants
from app.services import user_service
from app.services import review_service
from app.services import resto_service
from app.utils import jwt_required
from app.utils.jwt_utils import get_user_id_from_token


@bp.route("/mypage", methods=["GET", "POST"])
@jwt_required
def mypage():
    user_id = get_user_id_from_token()

    if request.method == "POST":
        new_info = {
            "name": request.form.get(
                "name",
                ""
            ).strip(),

            "track": request.form.get(
                "track",
                ""
            ).strip(),

            "cohort": request.form.get(
                "cohort",
                ""
            ).strip(),

            "number": request.form.get(
                "number",
                ""
            ).strip()
        }

        pw = request.form.get(
            "pw",
            ""
        )

        pw_confirm = request.form.get(
            "pw_confirm",
            ""
        )

        if pw or pw_confirm:
            new_info["pw"] = pw
            new_info["pw_confirm"] = pw_confirm

        result = user_service.update_user_info(
            user_id,
            new_info
        )

        if not result["success"]:
            return redirect(
                f"/mypage?error={result['code']}"
            )

        return redirect("/mypage")

    user = user_service.get_user(
        user_id
    )

    if user is None:
        return redirect("/login")

    track_type = constants.TRACK_TYPE

    reviews = review_service.get_reviews_by_user(
        user_id
    )

    for review in reviews:
        resto = resto_service.get_resto_detail(
            str(review["resto"])
        )

        review["resto"] = {
            "name": (
                resto["name"]
                if resto
                else "삭제된 식당"
            )
        }

        review["like"] = review.get(
            "like",
            0
        )

    return render_template(
        "mypage.html",
        user=user,
        reviews=reviews,
        track_type=track_type
    )