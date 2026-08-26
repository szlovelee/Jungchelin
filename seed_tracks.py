from app.db.mongodb import db


tracks = [
    "SW-AI랩",
    "게임랩",
    "게임테크랩",
    "추가할 트랙명"
]


for name in tracks:
    db.track_types.update_one(
        {"name": name},
        {
            "$set": {
                "name": name,
                "is_active": True
            }
        },
        upsert=True
    )


print("트랙 타입 저장 완료")