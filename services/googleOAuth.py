from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

from core import settings

# Configure Authlib client once (module-level singleton)
_oauth = OAuth()
_oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


async def redirect_to_google(request: Request) -> RedirectResponse:
    """Return RedirectResponse that sends the user to Google consent screen."""
    return await _oauth.google.authorize_redirect(request, settings.GOOGLE_AUTH_REDIRECT_URI)


async def fetch_user_info(request: Request) -> dict:
    """After Google callback, exchange code for tokens and return user claims.

    Raises FastAPI HTTPException on OAuth errors.
    """
    try:
        token = await _oauth.google.authorize_access_token(request)
        user_info: dict | None = await _oauth.google.parse_id_token(request, token)
    except OAuthError as err:
        raise HTTPException(status_code=400, detail=f"OAuth error: {err.error}") from err

    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info from Google")

    return user_info


auth_service = {
    "redirect_to_google": redirect_to_google,
    "fetch_user_info": fetch_user_info,
}