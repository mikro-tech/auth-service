from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    # --- General ---
    PROJECT_NAME: str = "Auth Service"
    API_V1_PREFIX: str = "/api/v1"

    # --- Google OAuth ---
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_AUTH_REDIRECT_URI: str  # mis. https://auth.example.com/api/v1/auth/google/callback

    # --- JWT ---
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str = "HS256"

    # --- CORS ---
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl | str] = []

    # --- Misc ---
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """
    Cached accessor so we don’t re-parse env vars on every import.
    Usage:
        settings = get_settings()
        print(settings.PROJECT_NAME)
    """
    return Settings()