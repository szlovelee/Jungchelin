from flask import Blueprint


bp = Blueprint("routes", __name__)


from . import auth_routes
from . import page_route
from . import resto_routes
from . import review_routes
from . import mypage_routes