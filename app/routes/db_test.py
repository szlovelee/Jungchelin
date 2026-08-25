from . import bp
from app.services import user_service
from app.db import user_db

@bp.route('/test/join', methods=["GET", "POST"])
def test_join() :
  user = {
    'name' : "노도현",
    'track' : "SW-AI",
    'custom_id' : "dhdh",
    'pw' : "123123",
    'pw_confirm' : "123123"
  }

  joined = user_service.join_service(user)
  return joined

@bp.route('/test/login', methods=["GET"])
def test_login() : 
  ret = user_service.login('guswl', '1999')
  return ret

@bp.route('/test/update-user', methods=["GET", "POST"])
def test_update_user() : 
  user_id = user_db.read_by_custom_id('guswl')["_id"]
  new_info = {
    'name' : '현지',
    'pw' : '1234',
    'pw_confirm' : '1234'
  }

  return user_service.update_user_info(user_id, new_info)
  