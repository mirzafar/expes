from bson import ObjectId
from bson.errors import InvalidId

from app.db.mongo import get_db

COLLECTION = "categories"

# Дефолтные категории, создаются при регистрации пользователя
DEFAULT_CATEGORIES = [
    # Расходы
    {"name": "Еда", "type": "expense", "icon": "🍔"},
    {"name": "Транспорт", "type": "expense", "icon": "🚗"},
    {"name": "Жильё", "type": "expense", "icon": "🏠"},
    {"name": "Развлечения", "type": "expense", "icon": "🎮"},
    {"name": "Здоровье", "type": "expense", "icon": "💊"},
    {"name": "Покупки", "type": "expense", "icon": "🛍️"},
    # Доходы
    {"name": "Зарплата", "type": "income", "icon": "💼"},
    {"name": "Подработка", "type": "income", "icon": "💻"},
    {"name": "Подарок", "type": "income", "icon": "🎁"},
    {"name": "Инвестиции", "type": "income", "icon": "📈"},
]


def _collection():
    return get_db()[COLLECTION]


async def ensure_indexes() -> None:
    # Уникальность имени в рамках пользователя и типа
    await _collection().create_index(
        [("user_id", 1), ("type", 1), ("name", 1)], unique=True
    )


def _oid(value: str) -> ObjectId | None:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


async def seed_defaults(user_id: str) -> None:
    """Создаёт стартовый набор категорий для нового пользователя."""
    docs = [
        {"user_id": user_id, "name": c["name"], "type": c["type"], "icon": c["icon"]}
        for c in DEFAULT_CATEGORIES
    ]
    if docs:
        await _collection().insert_many(docs)


async def list_for_user(user_id: str, type_: str | None = None) -> list[dict]:
    query: dict = {"user_id": user_id}
    if type_ is not None:
        query["type"] = type_
    cursor = _collection().find(query).sort([("type", 1), ("name", 1)])
    return await cursor.to_list(length=500)


async def create(user_id: str, name: str, type_: str, icon: str | None) -> dict:
    doc = {"user_id": user_id, "name": name, "type": type_, "icon": icon}
    result = await _collection().insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


async def update(user_id: str, cat_id: str, changes: dict) -> dict | None:
    oid = _oid(cat_id)
    if oid is None:
        return None
    if not changes:
        return await _collection().find_one({"_id": oid, "user_id": user_id})
    return await _collection().find_one_and_update(
        {"_id": oid, "user_id": user_id},
        {"$set": changes},
        return_document=True,
    )


async def delete(user_id: str, cat_id: str) -> bool:
    oid = _oid(cat_id)
    if oid is None:
        return False
    result = await _collection().delete_one({"_id": oid, "user_id": user_id})
    return result.deleted_count == 1
