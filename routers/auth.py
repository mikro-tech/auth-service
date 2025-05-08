from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from core import create_access_token, settings
from services.googleOauth import fetch_user_info, redirect_to_google

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------- Endpoints ----------
@router.get("/login/google", summary="Redirect user to Google OAuth consent screen")
async def login_with_google(request: Request) -> RedirectResponse:
    """Step-1: Redirect user to Google for authentication."""
    return await redirect_to_google(request)


@router.get("/login/google/callback", summary="Handle Google OAuth callback & issue JWT")
async def google_callback(request: Request):
    """Step-2: Handle Google callback, exchange code, and issue our JWT."""
    user_info = await fetch_user_info(request)
    jwt_token = create_access_token(user_info["sub"])
    return {"access_token": jwt_token, "token_type": "bearer"}