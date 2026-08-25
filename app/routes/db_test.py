from . import bp
from app.services import review_service, user_service, resto_service
from app.db import user_db, resto_db, review_db

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

@bp.route('/test/resto/star', methods=["GET"])
def avg_review():
  resto_id = resto_db.read_resto_list()[0]["_id"]
  return {
   'star' : resto_service.get_resto_star(resto_id)
  }


@bp.route('/test/review/add', methods=["GET","POST"])
def add_review():
  resto_id = resto_db.read_resto_list()[0]["_id"]
  user_id = user_db.read_by_custom_id('guswl')["_id"]
  comment = '수제비를 직접 만들면 수제수제비'
  return review_service.add_review(resto_id, user_id, comment, 5)

@bp.route('/test/review/like', methods=["GET", "POST"])
def toggle_like():
  user_id = user_db.read_by_custom_id('guswl')["_id"]
  writer = user_db.read_by_custom_id('dhdh')["_id"]
  review_id = review_db.read_reviews_by_user(writer)[0]["_id"]
  if review_service.user_liked(review_id, user_id) : 
    review_db.update_like_cancel(review_id, user_id)
  else :
    review_db.update_like_add(review_id, user_id)

  return str(review_db.read_review(review_id)["like"])