from app.db.mongodb import db


collection = db.track_types


def read_active_tracks():
    return list(
        collection.find(
            {"is_active": True}
        ).sort("name", 1)
    )


def create_track(name):
    return collection.insert_one({
        "name": name,
        "is_active": True
    })