from flask import (
    render_template,
    request,
    redirect,
    make_response
)

from . import bp
from app import constants
from app.services import auth_service
from app.utils.jwt_utils import create_token


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template(
            "login.html"
        )

    custom_id = request.form.get(
        "custom_id",
        ""
    ).strip()

    pw = request.form.get(
        "pw",
        ""
    )

    if not custom_id or not pw:
        return render_template(
            "login.html",
            error="아이디와 비밀번호를 입력해주세요."
        )

    result = auth_service.login(
        custom_id,
        pw
    )

    if not result["success"]:
        return render_template(
            "login.html",
            error=result["msg"]
        )

    token = create_token(
        result["user_id"]
    )

    response = make_response(
        redirect("/home")
    )

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 2
    )

    return response


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    track_type = constants.TRACK_TYPE

    if request.method == "GET":
        return render_template(
            "signup.html",
            track_type=track_type
        )

    user = {
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
        ).strip(),

        "custom_id": request.form.get(
            "custom_id",
            ""
        ).strip(),

        "pw": request.form.get(
            "pw",
            ""
        ),

        "pw_confirm": request.form.get(
            "pw_confirm",
            ""
        )
    }

    if not all(user.values()):
        return render_template(
            "signup.html",
            track_type=track_type,
            error="모든 항목을 입력해주세요."
        )

    if user["track"] not in track_type:
        return render_template(
            "signup.html",
            track_type=track_type,
            error="올바른 소속을 선택해주세요."
        )

    result = auth_service.join_service(
        user
    )

    if not result["success"]:
        return render_template(
            "signup.html",
            track_type=track_type,
            error=result["msg"]
        )

    return redirect("/login")


@bp.route("/logout", methods=["POST"])
def logout():
    response = make_response(
        redirect("/login")
    )

    response.delete_cookie(
        "access_token"
    )

    return response