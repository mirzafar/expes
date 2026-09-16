from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import ACCESS, decode_token
from app.repositories import user_repo

# tokenUrl нужен только для кнопки Authorize в Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

_credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не удалось проверить учётные данные",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Достаёт пользователя из access-токена. Иначе — 401."""
    user_id = decode_token(token, ACCESS)
    if user_id is None:
        raise _credentials_error
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise _credentials_error
    return user
