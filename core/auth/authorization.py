"""Authorization utilities for access control."""

from fastapi import Depends

from core.auth.authentication import (
    AuthenticatedUser,
    create_api_key_validator,
    verify_api_key,
)


def create_auth_dependency(endpoint_keys: str | None = None):
    """Create an auth dependency with optional endpoint-specific keys.

    Args:
        endpoint_keys: Optional endpoint-specific API keys

    Returns:
        A dependency function that requires authentication
    """
    validator = create_api_key_validator(endpoint_keys)

    async def require_auth_with_keys(
        api_key: str = Depends(validator),
    ) -> AuthenticatedUser:
        """Dependency that requires authentication.

        Args:
            api_key: Validated API key from authentication

        Returns:
            AuthenticatedUser instance
        """
        return AuthenticatedUser(api_key)

    return require_auth_with_keys


async def require_auth(
    api_key: str = Depends(verify_api_key),
) -> AuthenticatedUser:
    """Dependency that requires authentication (using global keys).

    This dependency will raise an AuthenticationError if the request
    is not authenticated.

    Args:
        api_key: Validated API key

    Returns:
        AuthenticatedUser instance

    Raises:
        AuthenticationError: If authentication fails
    """
    return AuthenticatedUser(api_key)
