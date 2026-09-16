import json

from app.db.redis import get_redis

# Кэш живёт недолго как страховка; основная свежесть — за счёт инвалидации при записи
DEFAULT_TTL = 300  # секунд


async def cache_get(key: str) -> dict | None:
    """Возвращает распарсенное значение из кэша или None."""
    raw = await get_redis().get(key)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


async def cache_set(key: str, value: dict, ttl: int = DEFAULT_TTL) -> None:
    """Кладёт значение в кэш с временем жизни."""
    await get_redis().set(key, json.dumps(value), ex=ttl)


async def invalidate_prefix(prefix: str) -> int:
    """Удаляет все ключи с данным префиксом. Возвращает число удалённых.
    Используем SCAN (не KEYS), чтобы не блокировать Redis на больших наборах."""
    redis = get_redis()
    deleted = 0
    async for key in redis.scan_iter(match=f"{prefix}*", count=100):
        await redis.delete(key)
        deleted += 1
    return deleted


def stats_prefix(user_id: str) -> str:
    """Общий префикс для всей кэшированной статистики пользователя.
    Инвалидируется целиком при любом изменении операций."""
    return f"stats:{user_id}:"


def _range(date_from, date_to) -> str:
    df = date_from.isoformat() if date_from else "-"
    dt = date_to.isoformat() if date_to else "-"
    return f"{df}:{dt}"


def summary_key(user_id: str, date_from, date_to) -> str:
    return f"stats:{user_id}:summary:{_range(date_from, date_to)}"


def by_category_key(user_id: str, type_: str, date_from, date_to) -> str:
    return f"stats:{user_id}:bycat:{type_}:{_range(date_from, date_to)}"


def timeseries_key(user_id: str, date_from) -> str:
    df = date_from.isoformat() if date_from else "-"
    return f"stats:{user_id}:ts:{df}"
