from app.db import user_db

def login(custom_id : str, pw : str):
  user = user_db.read_by_custom_id(custom_id)
  if user is None :
    return {
      'success' : False,
      'code' : "ID_NOT_FOUND",
      'msg' : "존재하지 않는 ID입니다."
    }

  if user["pw"] != pw :
    return {
      'success' : False,
      'code' : "PW_WRONG",
      'msg' : "비밀번호를 확인하십시오."
    }

  return { 'success' : True }


def join_service(user):
  if not check_id_duplication(user["custom_id"]) : 
    return {
      'success' : False,
      'code' : "ID_DUPLICATION",
      'msg' : "사용 중인 아이디입니다."
    }
  
  if user["pw"] != user["pw_confirm"] :
    return {
      'success' : False,
      'code' : "PW_MISMATCH",
      'msg' : "비밀번호가 일치하지 않습니다."
    }

  del user['pw_confirm']
  
  user_db.create_user(user)
  return { 'success' : True }

def check_id_duplication(custom_id : str) :
  return user_db.read_by_custom_id(custom_id) is None

def get_user_name(id : str):
  user = user_db.read_user(id)

  if user is None:
    return None
  
  return user['name']

def update_user_info(id: str, new_info):
  user =  user_db.read_user(id)

  # 사용자 확인
  if user is None :
    return {
      'success' : False,
      'code' : "USER_NOT_FOUND",
      'msg' : "해당 ID의 유저가 존재하지 않습니다."
    } 

  # 입력값이 유효한지 확인
  new_data = {}
  updates = 0

  def validate_info(key : str):
    if key in new_info and new_info[key] != user[key]:
        new_data[key] = new_info[key]
        return 1

    return 0

  updates += validate_info('name')
  updates += validate_info('track')
  updates += validate_info('cohort')
  updates += validate_info('number')

  # 비밀번호 확인 (있을 경우)
  if 'pw' in new_info :
    if 'pw_confirm' not in new_info or new_info["pw"] != new_info["pw_confirm"] :
      return {
        'success' : False,
        'code' : "PW_MISMATCH",
        'msg' : "비밀번호가 일치하지 않습니다."
      }
    else :
      updates += validate_info('pw')


  if not new_info or updates == 0:
    return {
      'success' : False,
      'code' : "NO_UPDATES",
      'msg' : "수정할 정보가 없습니다."
    }
  
  if user_db.update_user(id, new_info) is None :
    return {
      'success' : False,
      'code' : "DATABASE_FAILED",
      'msg' : "데이터 저장에 실패했습니다."
    }
  
  return {
    'success' : True
  }