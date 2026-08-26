from bson.objectid import ObjectId
from bson.errors import InvalidId

from app.db import review_db


def add_review(resto_id, user_id, comment, star):
    try:
        resto_object_id = ObjectId(resto_id)
        user_object_id = ObjectId(user_id)
    except (InvalidId, TypeError):
        return {
            "success": False,
            "code": "INVALID_ID",
            "msg": "잘못된 식당 또는 사용자 정보입니다."
        }

    if user_reviewed(resto_id, user_id):
        return {
            "success": False,
            "code": "REVIEW_DUPLICATION",
            "msg": "이미 작성한 리뷰가 있습니다."
        }

    review = {
        "resto": resto_object_id,
        "user": user_object_id,
        "comment": comment,
        "star": star,
        "like": 0,
        "liked": []
    }

    review_db.create_review(
        review
    )

    return {
        "success": True
    }


def get_review_list(resto_id):
    return list(
        review_db.read_reviews_by_resto(
            resto_id
        )
    )


def get_reviews_by_user(user_id):
    return list(
        review_db.read_reviews_by_user(
            user_id
        )
    )


def get_avg_star(resto_id):
    result = review_db.aggregate_avg_star(
        resto_id
    )

    if not result:
        return 0

    return round(
        result[0]["avg"],
        1
    )


def get_review_count(resto_id):
    return review_db.count_reviews_by_resto(
        resto_id
    )


def user_reviewed(resto_id, user_id):
    review = review_db.read_review_by_resto_and_user(
        resto_id,
        user_id
    )

    return review is not None


def toggle_like(review_id, user_id):
    try:
        review = review_db.read_review(
            review_id
        )

        user_object_id = ObjectId(
            user_id
        )
    except (InvalidId, TypeError):
        review = None

    if review is None:
        return {
            "success": False,
            "code": "REVIEW_NOT_FOUND"
        }

    liked_users = review.get(
        "liked",
        []
    )

    status = False
    if user_object_id in liked_users:
        review_db.update_like_cancel(
            review_id,
            user_id
        )
    else:
        review_db.update_like_add(
            review_id,
            user_id
        )
        status = True


    return {
        "success": True,
        "resto_id": str(review["resto"]),
        "status":status
    }


def edit_review(review_id, user_id, comment, star):
    try:
        review = review_db.read_review(
            review_id
        )

        user_object_id = ObjectId(
            user_id
        )
    except (InvalidId, TypeError):
        review = None

    if review is None:
        return {
            "success": False,
            "code": "REVIEW_NOT_FOUND"
        }

    if review["user"] != user_object_id:
        return {
            "success": False,
            "code": "NOT_REVIEW_OWNER"
        }

    review_db.update_review(
        review_id,
        {
            "comment": comment,
            "star": star
        }
    )

    return {
        "success": True
    }


def delete_review(review_id, user_id):
    try:
        review = review_db.read_review(
            review_id
        )

        user_object_id = ObjectId(
            user_id
        )
    except (InvalidId, TypeError):
        review = None

    if review is None:
        return {
            "success": False,
            "code": "REVIEW_NOT_FOUND"
        }

    if review["user"] != user_object_id:
        return {
            "success": False,
            "code": "NOT_REVIEW_OWNER"
        }

    review_db.delete_review(
        review_id
    )

    return {
        "success": True
    }