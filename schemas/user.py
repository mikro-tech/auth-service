from pydantic import BaseModel, EmailStr
from typing import Optional


class TokenPayload(BaseModel):
    """Internal model extracted from JWT claims."""

    sub: str  # subject (user id)
    exp: int  # expiration timestamp (Unix seconds)


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