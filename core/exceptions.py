"""Custom exception classes for the API."""

from typing import Any, Dict, Optional


class APIException(Exception):
    """Base exception for all API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
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


class ValidationError(APIException):
    """Exception for validation errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize validation error.

        Args:
            message: Error message
            status_code: HTTP status code (default: 400)
            details: Additional error details
        """
        super().__init__(message, status_code, details)


class NotFoundError(APIException):
    """Exception for resource not found errors."""

    def __init__(
        self,
        message: str = "Resource not found",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize not found error.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, 404, details, error_code="ERR_NOT_FOUND")


class AuthenticationError(APIException):
    """Exception for authentication errors."""

    def __init__(
        self,
        message: str = "Authentication required",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize authentication error.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, 401, details, error_code="ERR_AUTH")


class AuthorizationError(APIException):
    """Exception for authorization errors."""

    def __init__(
        self,
        message: str = "Insufficient permissions",
        details: Optional[Dict[str, Any]] = None,
    ):
        """Initialize authorization error.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, 403, details, error_code="ERR_AUTHORIZATION")

