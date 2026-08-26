from app.db import resto_db
from app.services import user_service


def add_resto(resto, user_id: str):
    if not check_address_duplication(resto["addr"]):
        return {
            "success": False,
            "code": "ADDR_DUPLICATION",
            "msg": "이미 존재하는 주소입니다."
        }

    resto_db.create_resto(resto, user_id)

    return {
        "success": True
    }


def check_address_duplication(addr: str):
    return resto_db.read_by_addr(addr) is None


def load_resto_list(sort_key=None):
    restaurants = list(resto_db.read_resto_list())

    if sort_key == "name":
        restaurants.sort(
            key=lambda restaurant: restaurant.get("name", "")
        )
        
    return restaurants


def get_resto_detail(resto_id: str):
    resto = resto_db.read_resto(resto_id)

    if resto is None:
        return None

    user_name = user_service.get_user_name(
        str(resto["user"])
    )

    resto["creator_name"] = user_name

    return resto


def get_resto_name(resto_id: str):
    resto = resto_db.read_resto(resto_id)

    if resto is None:
        return None

    return resto["name"]

def get_resto_star(id:str):
  resto = resto_db.read_resto(id)

  if 'star_sum' not in resto:
    return 0
  
  return round(resto['star_sum'] / resto['review_count'], 1)


def add_star_info(id:str, star:int):
  return resto_db.update_star(id, 1, star)

def update_star_info(id:str, prev:int, new:int):
  difference = new - prev
  return resto_db.update_star(id, 0, difference)

