from app.db import user_db

def check_id_duplication(custom_id : str) :
  return user_db.read_by_custom_id(custom_id) is None

def get_user_name(id : str):
  user = user_db.read_user(id)

  if user is None:
    return None
  
  return user['name']

def update_user_info(id: str, new_info):
  id_validity = verify_id(id)
  if not id_validity['success']:
    return id_validity

  
  # 입력값이 유효한지 확인
  user =  user_db.read_user(id)
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

def verify_id(id :str):
  if user_db.read_user(id) is None:
    return {
      'success' : False,
      'code' : "USER_NOT_FOUND",
      'msg' : "해당 ID의 사용자가 존재하지 않습니다."
    }

  return {
    'success' : True 
  }