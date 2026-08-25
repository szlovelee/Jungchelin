from . import bp
from app.services import user_service, resto_service
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


@bp.route('/test/resto/add', methods=["GET", "POST"])
def add_resto() :
  resto = {
    'name' : '북창동곱창',
    'addr' : '경기 용인시 처인구 포곡읍 포곡로 86 1층',
    'type' : '한식'
  }

  user_id = user_db.read_by_custom_id('guswl')["_id"]
  return resto_service.add_resto(resto, user_id)

@bp.route('/test/resto/list', methods=["GET"])
def load_resto_list() :
  lst = list(resto_service.load_resto_list())
  data = []
  for resto in lst:
    detail = resto_service.get_resto_detail(resto['_id'])
    info = {
      'name' : detail['name'],
      'user' : detail['user']
    }
    data.append(info)
  return data
  