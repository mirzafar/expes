from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_current_user
from app.core.cache import (
    by_category_key,
    cache_get,
    cache_set,
    summary_key,
    timeseries_key,
)
from app.models.transaction import CategorySlice, MonthPoint, Summary, TxType
from app.repositories import transaction_repo

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary", response_model=Summary)
async def get_summary(
    user: dict = Depends(get_current_user),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
) -> Summary:
    """Сводка: доход, расход, остаток и число операций за период.
    Результат кэшируется в Redis, инвалидируется при изменении операций."""
    user_id = str(user["_id"])
    key = summary_key(user_id, date_from, date_to)

    cached = await cache_get(key)
    if cached is not None:
        return Summary(**cached)

    data = await transaction_repo.summary(user_id, date_from=date_from, date_to=date_to)
    await cache_set(key, data)
    return Summary(**data)


@router.get("/by-category", response_model=list[CategorySlice])
async def get_by_category(
    user: dict = Depends(get_current_user),
    type: TxType = Query(default="expense", description="Тип операций для разбивки"),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
) -> list[CategorySlice]:
    """Суммы по категориям (для круговой диаграммы)."""
    user_id = str(user["_id"])
    key = by_category_key(user_id, type, date_from, date_to)

    cached = await cache_get(key)
    if cached is not None:
        return [CategorySlice(**row) for row in cached]

    data = await transaction_repo.by_category(
        user_id, type_=type, date_from=date_from, date_to=date_to
    )
    await cache_set(key, data)
    return [CategorySlice(**row) for row in data]


@router.get("/timeseries", response_model=list[MonthPoint])
async def get_timeseries(
    user: dict = Depends(get_current_user),
    months: int = Query(default=6, ge=1, le=24, description="Сколько последних месяцев"),
) -> list[MonthPoint]:
    """Доход и расход по месяцам (для графика тренда)."""
    user_id = str(user["_id"])

    # Начало периода: первый день месяца (months-1) назад
    now = datetime.now(timezone.utc)
    month0 = now.month - (months - 1)
    year = now.year + (month0 - 1) // 12
    month = (month0 - 1) % 12 + 1
    date_from = datetime(year, month, 1, tzinfo=timezone.utc)

    key = timeseries_key(user_id, date_from)
    cached = await cache_get(key)
    if cached is not None:
        return [MonthPoint(**row) for row in cached]

    data = await transaction_repo.timeseries(user_id, date_from=date_from)
    await cache_set(key, data)
    return [MonthPoint(**row) for row in data]
