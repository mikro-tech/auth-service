# Token / user schemas
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class TokenPayload(BaseModel):
    """Internal model extracted from JWT claims (mirrors JWT claims)."""

    sub: str  # subject (user id)
    exp: datetime  # expiration as datetime per RFC 7519


class TokenResponse(BaseModel):
    """JSON returned to client after successful login."""

    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    """Public user profile returned by this service (optional)."""

    id: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    picture: Optional[str] = None

    class Config:
        orm_mode = True