from datetime import datetime, timedelta
from typing import Any, Union

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from ..schemas.user import TokenPayload  # pastikan TokenPayload ada
from .config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- Password helpers ----------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ---------- JWT helpers ----------
def _build_jwt_payload(subject: Union[str, Any], expires_delta: int | None = None) -> dict[str, Any]:
    expire = datetime.utcnow() + (
        timedelta(minutes=expires_delta)
        if expires_delta is not None
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"sub": str(subject), "exp": expire}


def create_access_token(subject: Union[str, Any], expires_delta: int | None = None) -> str:
    payload = _build_jwt_payload(subject, expires_delta)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return TokenPayload(**payload)
    except (JWTError, ValidationError):
        return None