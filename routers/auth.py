from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

from core import create_access_token, settings

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------- OAuth client setup ----------
oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# ---------- Endpoints ----------
@router.get("/login/google", summary="Redirect user to Google OAuth consent screen")
async def login_with_google(request: Request) -> RedirectResponse:
    """
    Step-1: Redirect user to Google for authentication.
    """
    redirect_uri = settings.GOOGLE_AUTH_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/login/google/callback", summary="Handle Google OAuth callback & issue JWT")
async def google_callback(request: Request):
    """
    Step-2: Google redirects back with ?code=... .
    Exchange code for tokens, parse `id_token`, then mint our own JWT.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as err:
        raise HTTPException(status_code=400, detail=f"OAuth error: {err.error}")

    user_info = await oauth.google.parse_id_token(request, token)
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")

    # `sub` = stable Google user ID. Could also use email.
    jwt_token = create_access_token(user_info["sub"])
    return {"access_token": jwt_token, "token_type": "bearer"}