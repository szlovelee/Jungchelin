from app.db import review_db
from bson.objectid import ObjectId

def add_review(resto_id:str, user_id:str, comment:str, star:int):
  if user_reviewed(resto_id, user_id) :
    return {
      'success' : False,
      'code' : "REVIEW_DUPLICATION",
      'msg' : "이미 등록한 리뷰가 존재합니다."
    }
  
  review = {
    'resto' : ObjectId(resto_id),
    'user' : ObjectId(user_id),
    'comment' : comment,
    'star' : star
  }

  review_db.create_review(review)

  return {
    'success' : True
  }
    

def get_review_list(resto_id : str):
  return review_db.read_reviews_by_resto(resto_id)

def edit_review(id: str, comment:str, star:int):
  return review_db.update_review(id, {'comment':comment, 'star':star})

def delete_review(id : str ):
  return review_db.delete_review(id)

def user_reviewed(resto_id : str, user_id : str):
  review = review_db.read_review_by_resto_and_user(resto_id, user_id)
  return review is not None

def user_liked(id : str, user_id : str):
  review = review_db.read_review(id)
  if 'liked' not in review:
    return False
  return ObjectId(user_id) in review['liked']

def get_avg_star(resto_id : str):
  return review_db.aggregate_avg_star(resto_id)