from flask import Blueprint

bp = Blueprint('routes', __name__)

from . import db_test
