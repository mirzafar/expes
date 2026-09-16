from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from app.db.mongo import get_db

COLLECTION = "users"


def _collection():
    return get_db()[COLLECTION]


async def ensure_indexes() -> None:
    """Уникальный индекс на email — не даёт зарегистрировать два одинаковых."""
    await _collection().create_index("email", unique=True)


async def get_by_email(email: str) -> dict | None:
    return await _collection().find_one({"email": email})


async def get_by_id(user_id: str) -> dict | None:
    try:
        oid = ObjectId(user_id)
    except (InvalidId, TypeError):
        return None
    return await _collection().find_one({"_id": oid})


async def create(email: str, password_hash: str, name: str) -> dict:
    doc = {
        "email": email,
        "password_hash": password_hash,
        "name": name,
        "created_at": datetime.now(timezone.utc),
    }
    result = await _collection().insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc
