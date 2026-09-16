from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from app.db.mongo import get_db

COLLECTION = "transactions"


def _collection():
    return get_db()[COLLECTION]


async def ensure_indexes() -> None:
    """Индексы под частые запросы: операции пользователя, отсортированные по дате."""
    await _collection().create_index([("user_id", 1), ("date", -1)])
    await _collection().create_index([("user_id", 1), ("type", 1)])


def _oid(value: str) -> ObjectId | None:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


def _build_filter(
    user_id: str,
    *,
    type_: str | None = None,
    category: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> dict:
    """Собирает Mongo-фильтр по пользователю и опциональным критериям."""
    query: dict = {"user_id": user_id}
    if type_ is not None:
        query["type"] = type_
    if category is not None:
        query["category"] = category
    if date_from is not None or date_to is not None:
        date_query: dict = {}
        if date_from is not None:
            date_query["$gte"] = date_from
        if date_to is not None:
            date_query["$lte"] = date_to
        query["date"] = date_query
    return query


async def create(user_id: str, data: dict) -> dict:
    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user_id,
        "amount": data["amount"],
        "type": data["type"],
        "category": data.get("category"),
        "date": data.get("date") or now,
        "note": data.get("note"),
        "created_at": now,
    }
    result = await _collection().insert_one(doc)
    doc["_id"] = result.inserted_id
    return doc


async def list_for_user(
    user_id: str,
    *,
    type_: str | None = None,
    category: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    limit: int = 50,
    skip: int = 0,
) -> list[dict]:
    query = _build_filter(
        user_id, type_=type_, category=category, date_from=date_from, date_to=date_to
    )
    cursor = _collection().find(query).sort("date", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


async def get_one(user_id: str, tx_id: str) -> dict | None:
    oid = _oid(tx_id)
    if oid is None:
        return None
    return await _collection().find_one({"_id": oid, "user_id": user_id})


async def update(user_id: str, tx_id: str, changes: dict) -> dict | None:
    oid = _oid(tx_id)
    if oid is None:
        return None
    if not changes:
        return await _collection().find_one({"_id": oid, "user_id": user_id})
    return await _collection().find_one_and_update(
        {"_id": oid, "user_id": user_id},
        {"$set": changes},
        return_document=True,
    )


async def delete(user_id: str, tx_id: str) -> bool:
    oid = _oid(tx_id)
    if oid is None:
        return False
    result = await _collection().delete_one({"_id": oid, "user_id": user_id})
    return result.deleted_count == 1


async def summary(
    user_id: str,
    *,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> dict:
    """Считает суммы доходов/расходов за период одним запросом (агрегация)."""
    match = _build_filter(user_id, date_from=date_from, date_to=date_to)
    pipeline = [
        {"$match": match},
        {"$group": {"_id": "$type", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}},
    ]
    income = 0.0
    expense = 0.0
    count = 0
    async for row in _collection().aggregate(pipeline):
        count += row["count"]
        if row["_id"] == "income":
            income = row["total"]
        elif row["_id"] == "expense":
            expense = row["total"]
    return {
        "total_income": round(income, 2),
        "total_expense": round(expense, 2),
        "balance": round(income - expense, 2),
        "count": count,
    }


async def by_category(
    user_id: str,
    *,
    type_: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[dict]:
    """Суммы по категориям для заданного типа (доход/расход). Для donut-графика."""
    match = _build_filter(user_id, type_=type_, date_from=date_from, date_to=date_to)
    pipeline = [
        {"$match": match},
        {
            "$group": {
                "_id": {"$ifNull": ["$category", "Без категории"]},
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"total": -1}},
    ]
    result = []
    async for row in _collection().aggregate(pipeline):
        result.append(
            {"category": row["_id"], "total": round(row["total"], 2), "count": row["count"]}
        )
    return result


async def timeseries(user_id: str, *, date_from: datetime) -> list[dict]:
    """Доход и расход по месяцам начиная с date_from. Для area-графика и трендов."""
    pipeline = [
        {"$match": {"user_id": user_id, "date": {"$gte": date_from}}},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$date"},
                    "month": {"$month": "$date"},
                },
                "income": {
                    "$sum": {"$cond": [{"$eq": ["$type", "income"]}, "$amount", 0]}
                },
                "expense": {
                    "$sum": {"$cond": [{"$eq": ["$type", "expense"]}, "$amount", 0]}
                },
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]
    result = []
    async for row in _collection().aggregate(pipeline):
        y = row["_id"]["year"]
        m = row["_id"]["month"]
        result.append(
            {
                "period": f"{y:04d}-{m:02d}",
                "income": round(row["income"], 2),
                "expense": round(row["expense"], 2),
            }
        )
    return result
