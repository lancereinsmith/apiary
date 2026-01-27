"""Authentication utilities for API key validation."""

from fastapi import Depends, Header
from fastapi.security import APIKeyHeader

from config import Settings, get_settings
from core import AuthenticationError
from core.api_key_manager import get_api_key_manager

# API Key header name
API_KEY_HEADER = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


async def get_api_key_from_header(
    x_api_key: str | None = Header(None, alias="X-API-Key"),
) -> str | None:
    """Extract API key from request header.

    Args:
        x_api_key: API key from X-API-Key header

    Returns:
        API key string or None if not provided
    """
    return x_api_key


def validate_api_key(
    api_key: str, settings: Settings, endpoint_keys: str | None = None
) -> bool:
    """Validate an API key against configured keys.

    Args:
        api_key: The API key to validate
        settings: Application settings containing global API keys
        endpoint_keys: Optional endpoint-specific API keys (overrides global keys)

    Returns:
        True if the API key is valid, False otherwise
    """
    manager = get_api_key_manager()

    # If endpoint has specific keys, use those exclusively
    if endpoint_keys:
        return manager.validate_key(api_key, endpoint_keys)

    # Otherwise, use global keys
    if not settings.api_keys:
        # No API keys configured, authentication disabled
        return False

    return manager.validate_key(api_key, settings.api_keys)


def create_api_key_validator(endpoint_keys: str | None = None):
    """Create an API key validator dependency with optional endpoint-specific keys.

    Args:
        endpoint_keys: Optional endpoint-specific API keys

    Returns:
        A dependency function for API key validation
    """

    async def verify_api_key(
        api_key: str | None = Depends(get_api_key_from_header),
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

        if not validate_api_key(api_key, settings, endpoint_keys):
            raise AuthenticationError(
                "Invalid API key",
                details={"header": API_KEY_HEADER},
            )

        return api_key

    return verify_api_key


async def verify_api_key(
    api_key: str | None = Depends(get_api_key_from_header),
    settings: Settings = Depends(get_settings),
) -> str:
    """Default dependency to verify API key authentication using global keys.

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


def create_optional_authenticator(endpoint_keys: str | None = None):
    """Create an optional authenticator with endpoint-specific keys.

    Args:
        endpoint_keys: Optional endpoint-specific API keys

    Returns:
        A dependency function for optional authentication
    """

    async def get_authenticated_user(
        api_key: str | None = Depends(get_api_key_from_header),
        settings: Settings = Depends(get_settings),
    ) -> AuthenticatedUser | None:
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

        if validate_api_key(api_key, settings, endpoint_keys):
            return AuthenticatedUser(api_key)

        return None

    return get_authenticated_user


async def get_authenticated_user(
    api_key: str | None = Depends(get_api_key_from_header),
    settings: Settings = Depends(get_settings),
) -> AuthenticatedUser | None:
    """Get authenticated user from API key (optional) using global keys.

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
