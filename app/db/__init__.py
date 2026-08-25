from flask import Blueprint

bp = Blueprint('db', __name__)

from . import user_db
from . import mongodb