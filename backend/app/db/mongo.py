from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class MongoState:
    """Держит подключение к MongoDB на всё время жизни приложения."""

    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None


mongo = MongoState()


async def connect_mongo() -> None:
    """Открывает подключение к Mongo при старте приложения."""
    mongo.client = AsyncIOMotorClient(settings.mongo_uri)
    mongo.db = mongo.client[settings.mongo_db]


async def close_mongo() -> None:
    """Закрывает подключение при остановке приложения."""
    if mongo.client is not None:
        mongo.client.close()
        mongo.client = None
        mongo.db = None


def get_db() -> AsyncIOMotorDatabase:
    """Возвращает объект базы данных для работы с коллекциями."""
    if mongo.db is None:
        raise RuntimeError("MongoDB не подключена. Проверь запуск приложения.")
    return mongo.db


async def ping_mongo() -> bool:
    """Проверка живости Mongo — используется в /health."""
    if mongo.client is None:
        return False
    try:
        await mongo.client.admin.command("ping")
        return True
    except Exception:
        return False
