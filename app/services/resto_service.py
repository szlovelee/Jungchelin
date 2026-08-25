from app.db import resto_db, user_db, review_db
from app import constants

def add_resto(resto, user_id : str) :

  if not check_address_duplication(resto['addr']) : 
    return {
      'success' : False,
      'code' : "ADDR_DUPLICATION",
      'msg' : "이미 존재하는 주소입니다."
    }

  resto_db.create_resto(resto, user_id)
  
  return {
    'success' : True
  }

def check_address_duplication(addr : str) :
  return resto_db.read_by_addr(addr) is None

def load_resto_list() :
  default_sort_key = constants.RESOT_SORT_DEFAULT
  default_sort_order = constants.RESTO_SORT[default_sort_key]['order']
  return resto_db.read_resto_list().sort(default_sort_key, default_sort_order)

def get_resto_detail(id : str) :
  detail = resto_db.read_resto(id)
  user_name = user_db.read_user(detail['user'])['name']
  detail['user'] = user_name
  return detail

def get_resto_name(id : str) :
  resto = resto_db.read_resto(id)
  return resto['name']

def get_resto_star(id : str):
  avg_result = review_db.aggregate_avg_star(id)

  if not avg_result:
    return 0

  return round(avg_result[0]['avg'], 1)