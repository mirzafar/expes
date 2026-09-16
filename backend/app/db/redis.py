import redis.asyncio as aioredis

from app.core.config import settings


class RedisState:
    """Держит подключение к Redis на всё время жизни приложения."""

    client: aioredis.Redis | None = None


redis_state = RedisState()


async def connect_redis() -> None:
    """Открывает подключение к Redis при старте приложения."""
    redis_state.client = aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )


async def close_redis() -> None:
    """Закрывает подключение при остановке приложения."""
    if redis_state.client is not None:
        await redis_state.client.aclose()
        redis_state.client = None


def get_redis() -> aioredis.Redis:
    """Возвращает Redis-клиент для кэширования."""
    if redis_state.client is None:
        raise RuntimeError("Redis не подключён. Проверь запуск приложения.")
    return redis_state.client


async def ping_redis() -> bool:
    """Проверка живости Redis — используется в /health."""
    if redis_state.client is None:
        return False
    try:
        return await redis_state.client.ping()
    except Exception:
        return False
