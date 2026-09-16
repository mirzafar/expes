import base64
import hashlib
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings

# Типы токенов — чтобы access нельзя было использовать вместо refresh и наоборот
ACCESS = "access"
REFRESH = "refresh"


def _prehash(password: str) -> bytes:
    """bcrypt ограничен 72 байтами. sha256 + base64 позволяет безопасно
    использовать пароль любой длины без молчаливого обрезания."""
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest)


def hash_password(password: str) -> str:
    """Возвращает bcrypt-хэш пароля для хранения в БД."""
    return bcrypt.hashpw(_prehash(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Проверяет введённый пароль против хэша из БД."""
    return bcrypt.checkpw(_prehash(plain), hashed.encode("utf-8"))


def _create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,          # id пользователя
        "type": token_type,      # access | refresh
        "iat": now,              # когда выпущен
        "exp": now + expires_delta,  # когда истекает
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: str) -> str:
    return _create_token(
        user_id, ACCESS, timedelta(minutes=settings.access_token_expire_minutes)
    )


def create_refresh_token(user_id: str) -> str:
    return _create_token(
        user_id, REFRESH, timedelta(days=settings.refresh_token_expire_days)
    )


def decode_token(token: str, expected_type: str) -> str | None:
    """Проверяет подпись и тип токена. Возвращает user_id или None."""
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except JWTError:
        return None
    if payload.get("type") != expected_type:
        return None
    user_id = payload.get("sub")
    if not isinstance(user_id, str):
        return None
    return user_id
