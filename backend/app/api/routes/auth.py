from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.errors import DuplicateKeyError

from app.api.deps import get_current_user
from app.core.security import (
    REFRESH,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import (
    RefreshRequest,
    TokenPair,
    UserPublic,
    UserRegister,
)
from app.repositories import category_repo, user_repo

router = APIRouter(prefix="/auth", tags=["auth"])


def _to_public(user: dict) -> UserPublic:
    return UserPublic(
        id=str(user["_id"]),
        email=user["email"],
        name=user["name"],
        created_at=user["created_at"],
    )


def _tokens_for(user_id: str) -> TokenPair:
    return TokenPair(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.post("/register", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister) -> TokenPair:
    """Регистрация нового пользователя. Возвращает пару токенов."""
    try:
        user = await user_repo.create(
            email=data.email,
            password_hash=hash_password(data.password),
            name=data.name,
        )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )
    # Стартовый набор категорий для нового пользователя
    await category_repo.seed_defaults(str(user["_id"]))
    return _tokens_for(str(user["_id"]))


@router.post("/login", response_model=TokenPair)
async def login(form: OAuth2PasswordRequestForm = Depends()) -> TokenPair:
    """Вход по email и паролю. Поле username в форме — это email."""
    user = await user_repo.get_by_email(form.username)
    if user is None or not verify_password(form.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )
    return _tokens_for(str(user["_id"]))


@router.post("/refresh", response_model=TokenPair)
async def refresh(data: RefreshRequest) -> TokenPair:
    """Обновление пары токенов по действующему refresh-токену."""
    user_id = decode_token(data.refresh_token, REFRESH)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh-токен",
        )
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )
    return _tokens_for(user_id)


@router.get("/me", response_model=UserPublic)
async def me(current_user: dict = Depends(get_current_user)) -> UserPublic:
    """Текущий пользователь по access-токену."""
    return _to_public(current_user)
