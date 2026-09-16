from fastapi import APIRouter

from app.db.mongo import ping_mongo
from app.db.redis import ping_redis

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    """Проверка состояния сервиса и его зависимостей (Mongo, Redis)."""
    mongo_ok = await ping_mongo()
    redis_ok = await ping_redis()
    all_ok = mongo_ok and redis_ok
    return {
        "status": "ok" if all_ok else "degraded",
        "services": {
            "mongo": "up" if mongo_ok else "down",
            "redis": "up" if redis_ok else "down",
        },
    }
