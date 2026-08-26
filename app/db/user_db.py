from bson.objectid import ObjectId
from bson.errors import InvalidId

from .mongodb import db


collection = db.users


def create_user(user):
    return collection.insert_one(user)


def read_user(user_id):
    try:
        object_id = ObjectId(user_id)
    except (InvalidId, TypeError):
        return None

    return collection.find_one({
        "_id": object_id
    })


def read_by_custom_id(custom_id):
    return collection.find_one({
        "custom_id": custom_id
    })


def update_user(user_id, new_info):
    try:
        object_id = ObjectId(user_id)
    except (InvalidId, TypeError):
        return None

    return collection.update_one(
        {
            "_id": object_id
        },
        {
            "$set": new_info
        }
    )