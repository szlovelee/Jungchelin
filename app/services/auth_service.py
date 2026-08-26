from app.db import user_db
from . import user_service

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

  return { 
    'success' : True,
    'user_id' :  user['_id']
  }

def join_service(user):
  if not user_service.check_id_duplication(user["custom_id"]) : 
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