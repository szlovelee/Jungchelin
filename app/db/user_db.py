from bson.objectid import ObjectId
from .mongodb import db

collection = db.users

def create_user(user):
  return collection.insert_one(user)
  

def read_user(id : str):
  return collection.find_one({'_id':ObjectId(id)})
  

def read_user_name(id : str):
  user = collection.find_one({'_id':ObjectId(id)})

  if user is None:
    return None
  
  return user['name']


def read_by_custom_id(custom_id : str):
  return collection.find_one({'custom_id' : custom_id})
    

def update_user(id : str, new_info):  
  return collection.update_one({'_id':ObjectId(id)}, {'$set':new_info})