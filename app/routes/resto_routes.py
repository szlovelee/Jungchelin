from flask import request

from . import bp
from app.services import resto_service, user_service
from app.utils.jwt_utils import get_user_id_from_token

@bp.route('resto/add', methods=["POST"])
def add_resto():
  user_id = get_user_id_from_token()

  resto = {
    'name': request.form.get("name").strip(),
    'addr': request.form.get("addr").strip()
  }    

  required_fields = [
    resto["name"],
    resto["addr"]
  ]

  if not all(required_fields):
    return {
      'success' : False,
      'code' : "REQUIRED_FIELDS",
      'msg' : "필수 항목을 채워주세요."
    }, 400
  
  result = resto_service.add_resto(resto, user_id)

  if not result['success']:
    return result, 409


  return result, 201

def get_resto_name(id):
  return None

