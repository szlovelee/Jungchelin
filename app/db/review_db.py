from bson.objectid import ObjectId
from pymongo import ReturnDocument

from .mongodb import db


collection = db.review


def create_review(review):
    return collection.insert_one(review)


def read_review(review_id):
    return collection.find_one({
        "_id": ObjectId(review_id)
    })


def read_reviews_by_resto(resto_id):
    return collection.find({
        "resto": ObjectId(resto_id)
    })


def read_reviews_by_user(user_id):
    return collection.find({
        "user": ObjectId(user_id)
    })


def count_reviews_by_resto(resto_id):
    return collection.count_documents({
        "resto": ObjectId(resto_id)
    })


def read_review_by_resto_and_user(resto_id, user_id):
    return collection.find_one({
        "resto": ObjectId(resto_id),
        "user": ObjectId(user_id)
    })


def update_review(review_id, content):
    return collection.find_one_and_update(
        {
            "_id": ObjectId(review_id)
        },
        {
            "$set": content
        },
        return_document=ReturnDocument.AFTER
    )


def update_like_add(review_id, user_id):
    return collection.find_one_and_update(
        {
            "_id": ObjectId(review_id)
        },
        {
            "$push": {
                "liked": ObjectId(user_id)
            },
            "$inc": {
                "like": 1
            }
        },
        return_document=ReturnDocument.AFTER
    )


def update_like_cancel(review_id, user_id):
    return collection.find_one_and_update(
        {
            "_id": ObjectId(review_id)
        },
        {
            "$pull": {
                "liked": ObjectId(user_id)
            },
            "$inc": {
                "like": -1
            }
        },
        return_document=ReturnDocument.AFTER
    )


def delete_review(review_id):
    return collection.delete_one({
        "_id": ObjectId(review_id)
    })


def aggregate_avg_star(resto_id):
    pipeline = [
        {
            "$match": {
                "resto": ObjectId(resto_id)
            }
        },
        {
            "$group": {
                "_id": None,
                "avg": {
                    "$avg": "$star"
                }
            }
        }
    ]

    return list(
        collection.aggregate(pipeline)
    )