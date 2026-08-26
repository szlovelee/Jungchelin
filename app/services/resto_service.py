from app import constants
from app.db import resto_db
from app.services import review_service
from app.services import user_service


def add_resto(resto, user_id):
    if not check_address_duplication(
        resto["addr"]
    ):
        return {
            "success": False,
            "code": "ADDR_DUPLICATION",
            "msg": "이미 존재하는 주소입니다."
        }

    resto_db.create_resto(
        resto,
        user_id
    )

    return {
        "success": True
    }


def check_address_duplication(addr):
    return resto_db.read_by_addr(
        addr
    ) is None


def load_resto_list(user_id, sort_key="star"):
    restaurants = list(
        resto_db.read_resto_list()
    )

    pinned = user_service.get_user_fav_resto(user_id)

    for restaurant in restaurants:
        resto_id = str(
            restaurant["_id"]
        )

        restaurant["average_rating"] = (
            review_service.get_avg_star(
                resto_id
            )
        )

        restaurant["review_count"] = (
            review_service.get_review_count(
                resto_id
            )
        )

    sort_option = constants.RESTO_SORT.get(sort_key,
                                            constants.RESTO_SORT[constants.RESOT_SORT_DEFAULT])

    field = sort_option["field"]
    order = sort_option["order"]

    if order == -1:
        restaurants.sort( 
            key=lambda restaurant: (
                restaurant["_id"] not in pinned,
                -restaurant.get(field,0)
            )
        )
    else:
        restaurants.sort(
            key=lambda restaurant: (
                restaurant["_id"] not in pinned,
                restaurant.get(field,"")
            )
        )

    return restaurants


def get_resto_detail(resto_id):
    resto = resto_db.read_resto(
        resto_id
    )

    if resto is None:
        return None

    resto["average_rating"] = (
        review_service.get_avg_star(
            resto_id
        )
    )

    resto["review_count"] = (
        review_service.get_review_count(
            resto_id
        )
    )

    resto["creator_name"] = (
        user_service.get_user_name(
            str(resto["user"])
        )
    )

    return resto


def get_resto_name(resto_id):
    resto = resto_db.read_resto(
        resto_id
    )

    if resto is None:
        return None

    return resto["name"]