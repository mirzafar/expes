from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_user
from app.core.cache import invalidate_prefix, stats_prefix
from app.models.transaction import (
    TransactionCreate,
    TransactionPublic,
    TransactionUpdate,
    TxType,
)
from app.repositories import transaction_repo

router = APIRouter(prefix="/transactions", tags=["transactions"])


def _to_public(doc: dict) -> TransactionPublic:
    return TransactionPublic(
        id=str(doc["_id"]),
        amount=doc["amount"],
        type=doc["type"],
        category=doc.get("category"),
        date=doc["date"],
        note=doc.get("note"),
        created_at=doc["created_at"],
    )


@router.post("", response_model=TransactionPublic, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    data: TransactionCreate,
    user: dict = Depends(get_current_user),
) -> TransactionPublic:
    """Создать операцию (приход или расход)."""
    user_id = str(user["_id"])
    doc = await transaction_repo.create(user_id, data.model_dump())
    await invalidate_prefix(stats_prefix(user_id))
    return _to_public(doc)


@router.get("", response_model=list[TransactionPublic])
async def list_transactions(
    user: dict = Depends(get_current_user),
    type: TxType | None = Query(default=None, description="Фильтр по типу"),
    category: str | None = Query(default=None),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    skip: int = Query(default=0, ge=0),
) -> list[TransactionPublic]:
    """Список операций пользователя с фильтрами и постраничностью."""
    docs = await transaction_repo.list_for_user(
        str(user["_id"]),
        type_=type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        skip=skip,
    )
    return [_to_public(d) for d in docs]


@router.get("/{tx_id}", response_model=TransactionPublic)
async def get_transaction(
    tx_id: str,
    user: dict = Depends(get_current_user),
) -> TransactionPublic:
    doc = await transaction_repo.get_one(str(user["_id"]), tx_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Операция не найдена")
    return _to_public(doc)


@router.put("/{tx_id}", response_model=TransactionPublic)
async def update_transaction(
    tx_id: str,
    data: TransactionUpdate,
    user: dict = Depends(get_current_user),
) -> TransactionPublic:
    """Изменить операцию. Передаются только меняемые поля."""
    user_id = str(user["_id"])
    changes = data.model_dump(exclude_unset=True)
    doc = await transaction_repo.update(user_id, tx_id, changes)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Операция не найдена")
    await invalidate_prefix(stats_prefix(user_id))
    return _to_public(doc)


@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    tx_id: str,
    user: dict = Depends(get_current_user),
) -> None:
    user_id = str(user["_id"])
    ok = await transaction_repo.delete(user_id, tx_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Операция не найдена")
    await invalidate_prefix(stats_prefix(user_id))
