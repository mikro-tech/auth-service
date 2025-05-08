"""
Shortcut imports so other modules can simply do:
    from core import settings, create_access_token
"""
from .config import get_settings
from .security import create_access_token, decode_access_token

settings = get_settings()

__all__ = [
    "settings",
    "create_access_token",
    "decode_access_token",
]