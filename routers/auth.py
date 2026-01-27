"""Authentication endpoints."""

import fastapi
from fastapi import Depends

from core.auth.authentication import AuthenticatedUser, get_authenticated_user
from core.auth.authorization import require_auth
from models.responses import BaseResponse

router = fastapi.APIRouter(tags=["authentication"])


class AuthStatusResponse(BaseResponse):
    """Response model for authentication status."""

    authenticated: bool
    message: str


@router.get(
    "/auth/status",
    response_model=AuthStatusResponse,
    summary="Check authentication status",
    description="Check if the current request is authenticated",
    responses={
        200: {
            "description": "Authentication status",
            "content": {
                "application/json": {
                    "example": {
                        "authenticated": True,
                        "message": "Authenticated",
                        "timestamp": "2024-01-01T12:00:00",
                    }
                }
            },
        }
    },
)
async def auth_status(
    user: AuthenticatedUser = Depends(require_auth),
) -> AuthStatusResponse:
    """Check authentication status.

    This endpoint requires authentication to access.

    Args:
        user: Authenticated user

    Returns:
        AuthStatusResponse with authentication status
    """
    return AuthStatusResponse(
        authenticated=True,
        message="Authenticated",
    )


@router.get(
    "/auth/validate",
    response_model=AuthStatusResponse,
    summary="Validate API key",
    description="Validate an API key without requiring authentication (optional auth)",
    responses={
        200: {
            "description": "Validation result",
            "content": {
                "application/json": {
                    "examples": {
                        "authenticated": {
                            "value": {
                                "authenticated": True,
                                "message": "Valid API key",
                                "timestamp": "2024-01-01T12:00:00",
                            }
                        },
                        "not_authenticated": {
                            "value": {
                                "authenticated": False,
                                "message": "No API key provided or invalid key",
                                "timestamp": "2024-01-01T12:00:00",
                            }
                        },
                    }
                }
            },
        }
    },
)
async def validate_api_key(
    user: AuthenticatedUser | None = Depends(get_authenticated_user),
) -> AuthStatusResponse:
    """Validate an API key (optional authentication).

    This endpoint can be called with or without authentication.
    It will return the authentication status.

    Args:
        user: Optional authenticated user

    Returns:
        AuthStatusResponse indicating if authenticated
    """
    if user:
        return AuthStatusResponse(
            authenticated=True,
            message="Valid API key",
        )
    else:
        return AuthStatusResponse(
            authenticated=False,
            message="No API key provided or invalid key",
        )
