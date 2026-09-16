from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, categories, health, stats, transactions
from app.core.config import settings
from app.db.mongo import close_mongo, connect_mongo
from app.db.redis import close_redis, connect_redis
from app.repositories import category_repo, transaction_repo, user_repo


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Открываем подключения при старте, закрываем при остановке."""
    await connect_mongo()
    await connect_redis()
    await user_repo.ensure_indexes()
    await transaction_repo.ensure_indexes()
    await category_repo.ensure_indexes()
    yield
    await close_redis()
    await close_mongo()


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(stats.router)
app.include_router(categories.router)


@app.get("/")
async def root() -> dict:
    return {"message": f"{settings.app_name} работает. Документация: /docs"}
