"""Authorization utilities for access control."""


from fastapi import Depends

from core.auth.authentication import AuthenticatedUser, verify_api_key


async def require_auth(
    api_key: str = Depends(verify_api_key),
) -> AuthenticatedUser:
    """Dependency that requires authentication.

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

