from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Данные для регистрации."""

    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    name: str = Field(min_length=1, max_length=100)


class UserLogin(BaseModel):
    """Данные для входа."""

    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """Пользователь в ответах API — без пароля."""

    id: str
    email: EmailStr
    name: str
    created_at: datetime


class TokenPair(BaseModel):
    """Пара токенов, выдаётся при логине/регистрации."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
