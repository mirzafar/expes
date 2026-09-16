from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

TxType = Literal["income", "expense"]


class TransactionCreate(BaseModel):
    """Данные для создания операции."""

    amount: float = Field(gt=0, description="Сумма операции, всегда положительная")
    type: TxType
    category: str | None = Field(default=None, max_length=100)
    date: datetime | None = Field(default=None, description="Если не указана — берётся текущее время")
    note: str | None = Field(default=None, max_length=500)


class TransactionUpdate(BaseModel):
    """Частичное обновление операции — все поля необязательны."""

    amount: float | None = Field(default=None, gt=0)
    type: TxType | None = None
    category: str | None = Field(default=None, max_length=100)
    date: datetime | None = None
    note: str | None = Field(default=None, max_length=500)


class TransactionPublic(BaseModel):
    """Операция в ответах API."""

    id: str
    amount: float
    type: TxType
    category: str | None = None
    date: datetime
    note: str | None = None
    created_at: datetime


class Summary(BaseModel):
    """Сводка за период."""

    total_income: float
    total_expense: float
    balance: float
    count: int


class CategorySlice(BaseModel):
    """Сумма по одной категории (для круговой диаграммы)."""

    category: str
    total: float
    count: int


class MonthPoint(BaseModel):
    """Доход и расход за один месяц (для графика тренда)."""

    period: str  # "YYYY-MM"
    income: float
    expense: float
