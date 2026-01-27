"""Custom exception classes for the API."""

from typing import Any


class APIError(Exception):
    """Base exception for all API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
        error_code: str | None = None,
    ):
        """Initialize API exception.

        Args:
            message: Human-readable error message
            status_code: HTTP status code
            details: Additional error details
            error_code: Optional error code for programmatic handling
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.error_code = error_code or f"ERR_{status_code}"


class ValidationError(APIError):
    """Exception for validation errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ):
        """Initialize validation error.

        Args:
            message: Error message
            status_code: HTTP status code (default: 400)
            details: Additional error details
        """
        super().__init__(message, status_code, details)


class NotFoundError(APIError):
    """Exception for resource not found errors."""

    def __init__(
        self,
        message: str = "Resource not found",
        details: dict[str, Any] | None = None,
    ):
        """Initialize not found error.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, 404, details, error_code="ERR_NOT_FOUND")


class AuthenticationError(APIError):
    """Exception for authentication errors."""

    def __init__(
        self,
        message: str = "Authentication required",
        details: dict[str, Any] | None = None,
    ):
        """Initialize authentication error.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, 401, details, error_code="ERR_AUTH")


class AuthorizationError(APIError):
    """Exception for authorization errors."""

    def __init__(
        self,
        message: str = "Insufficient permissions",
        details: dict[str, Any] | None = None,
    ):
        """Initialize authorization error.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, 403, details, error_code="ERR_AUTHORIZATION")
