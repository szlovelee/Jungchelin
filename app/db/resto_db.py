from bson.objectid import ObjectId
from pymongo import ReturnDocument
from .mongodb import db

collection = db.resto

def create_resto(resto, user_id):
  resto['user'] = ObjectId(user_id)
  return collection.insert_one(resto)

def read_resto_list():
  return collection.find({})

def read_resto(id : str):
  return collection.find_one({'_id' : ObjectId(id)})

def read_by_addr(addr : str):
  return collection.find_one({'addr' : addr})

def update_star(id:str, rv_count:int, star_amount:int):
  return collection.find_one_and_update({'_id':ObjectId(id)}, 
                               {'$inc':{'review_count': rv_count, 'star_sum':star_amount}}, 
                               return_document=ReturnDocument.AFTER)
