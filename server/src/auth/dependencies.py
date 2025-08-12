from datetime import datetime
from typing import Any

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth import service, jwt
from src.auth.exceptions import EmailTaken, RefreshTokenNotValid
from src.auth.schemas import AuthUser

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, Any]:
    try:
        token = credentials.credentials
        payload = jwt.decode_jwt(token)
        user = await service.get_user_by_id(payload.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

async def valid_user_create(user: AuthUser) -> AuthUser:
    if await service.get_user_by_email(user.email):
        raise EmailTaken()

    return user


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> dict[str, Any]:
    db_refresh_token = await service.get_refresh_token(refresh_token)
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> dict[str, Any]:
    user = await service.get_user_by_id(refresh_token["user_id"])
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: dict[str, Any]) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]
