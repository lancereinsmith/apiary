"""Authentication utilities for API key validation."""

from typing import Optional

from fastapi import Depends, Header
from fastapi.security import APIKeyHeader

from config import Settings, get_settings
from core import AuthenticationError

# API Key header name
API_KEY_HEADER = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


async def get_api_key_from_header(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
) -> Optional[str]:
    """Extract API key from request header.

    Args:
        x_api_key: API key from X-API-Key header

    Returns:
        API key string or None if not provided
    """
    return x_api_key


def validate_api_key(api_key: str, settings: Settings) -> bool:
    """Validate an API key against configured keys.

    Args:
        api_key: The API key to validate
        settings: Application settings containing valid API keys

    Returns:
        True if the API key is valid, False otherwise
    """
    if not settings.api_keys:
        # No API keys configured, authentication disabled
        return False

    # Split comma-separated keys and check for match
    valid_keys = [key.strip() for key in settings.api_keys.split(",") if key.strip()]
    return api_key in valid_keys


async def verify_api_key(
    api_key: Optional[str] = Depends(get_api_key_from_header),
    settings: Settings = Depends(get_settings),
) -> str:
    """Dependency to verify API key authentication.

    Args:
        api_key: API key from request header
        settings: Application settings

    Returns:
        The validated API key

    Raises:
        HTTPException: If authentication fails
    """
    if not api_key:
        raise AuthenticationError(
            "API key required",
            details={"header": API_KEY_HEADER},
        )

    if not validate_api_key(api_key, settings):
        raise AuthenticationError(
            "Invalid API key",
            details={"header": API_KEY_HEADER},
        )

    return api_key


class AuthenticatedUser:
    """Represents an authenticated user."""

    def __init__(self, api_key: str):
        """Initialize authenticated user.

        Args:
            api_key: The validated API key
        """
        self.api_key = api_key
        self.is_authenticated = True


async def get_authenticated_user(
    api_key: Optional[str] = Depends(get_api_key_from_header),
    settings: Settings = Depends(get_settings),
) -> Optional[AuthenticatedUser]:
    """Get authenticated user from API key (optional).

    This function does not raise an error if authentication fails.
    It returns None if the API key is missing or invalid.

    Args:
        api_key: API key from header (may be None)
        settings: Application settings

    Returns:
        AuthenticatedUser if authenticated, None otherwise
    """
    if not api_key:
        return None

    if validate_api_key(api_key, settings):
        return AuthenticatedUser(api_key)

    return None

