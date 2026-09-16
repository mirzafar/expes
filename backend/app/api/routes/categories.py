from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.errors import DuplicateKeyError

from app.api.deps import get_current_user
from app.models.category import (
    CategoryCreate,
    CategoryPublic,
    CategoryType,
    CategoryUpdate,
)
from app.repositories import category_repo

router = APIRouter(prefix="/categories", tags=["categories"])


def _to_public(doc: dict) -> CategoryPublic:
    return CategoryPublic(
        id=str(doc["_id"]),
        name=doc["name"],
        type=doc["type"],
        icon=doc.get("icon"),
    )


@router.get("", response_model=list[CategoryPublic])
async def list_categories(
    user: dict = Depends(get_current_user),
    type: CategoryType | None = Query(default=None, description="Фильтр по типу"),
) -> list[CategoryPublic]:
    docs = await category_repo.list_for_user(str(user["_id"]), type)
    return [_to_public(d) for d in docs]


@router.post("", response_model=CategoryPublic, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    user: dict = Depends(get_current_user),
) -> CategoryPublic:
    try:
        doc = await category_repo.create(str(user["_id"]), data.name, data.type, data.icon)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такая категория уже существует",
        )
    return _to_public(doc)


@router.put("/{cat_id}", response_model=CategoryPublic)
async def update_category(
    cat_id: str,
    data: CategoryUpdate,
    user: dict = Depends(get_current_user),
) -> CategoryPublic:
    changes = data.model_dump(exclude_unset=True)
    try:
        doc = await category_repo.update(str(user["_id"]), cat_id, changes)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такая категория уже существует",
        )
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return _to_public(doc)


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    cat_id: str,
    user: dict = Depends(get_current_user),
) -> None:
    ok = await category_repo.delete(str(user["_id"]), cat_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
