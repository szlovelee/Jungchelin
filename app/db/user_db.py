from bson.objectid import ObjectId
from pymongo import ReturnDocument

from .mongodb import db


collection = db.users


def create_user(user):
    return collection.insert_one(user)


def read_user(id:str):
    return collection.find_one({
        "_id": ObjectId(id)
    })


def read_by_custom_id(custom_id : str):
    return collection.find_one({
        "custom_id": custom_id
    })

def read_user_fav_resto(id :str):
    return collection.find_one({
        '_id':ObjectId(id)
    })


def update_user(id: str, new_info):
    return collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": new_info
        }
    )

def add_favorite_resto(id:str, resto_id :str):
    return collection.find_one_and_update(
        {
          '_id':ObjectId(id)
        },
        {
          '$push':
          {
              'fav_resto':ObjectId(resto_id)
           }
        },
        return_document=ReturnDocument.AFTER)

def remove_favorite_resto(id:str, resto_id :str):
    return collection.find_one_and_update(
        {
          '_id':ObjectId(id)
        },
        {
          '$pull':
          {
              'fav_resto':ObjectId(resto_id)
           }
        },
        return_document=ReturnDocument.AFTER)