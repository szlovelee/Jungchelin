from flask import render_template
from . import bp


@bp.route("/")
def index_page():
    return render_template("index.html")


@bp.route("/login")
def login_page():
    return render_template("login.html")


@bp.route("/home")
def home_page():
    return render_template("home.html")