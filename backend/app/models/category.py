from typing import Literal

from pydantic import BaseModel, Field

CategoryType = Literal["income", "expense"]


class CategoryCreate(BaseModel):
    """Данные для создания категории."""

    name: str = Field(min_length=1, max_length=50)
    type: CategoryType
    icon: str | None = Field(default=None, max_length=8)  # эмодзи


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    icon: str | None = Field(default=None, max_length=8)


class CategoryPublic(BaseModel):
    id: str
    name: str
    type: CategoryType
    icon: str | None = None
