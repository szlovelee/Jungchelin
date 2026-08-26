from app.db.mongodb import db

tracks = [
    "SW-AI랩",
    "게임랩",
    "게임테크랩"
]

for name in tracks:
    db.track_types.update_one(
        {"name": name},
        {
            "$setOnInsert": {
                "name": name,
                "is_active": True
            }
        },
        upsert=True
    )

print("소속 데이터 초기화 완료")