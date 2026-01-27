"""Request validation and sanitization utilities."""

import logging
from collections.abc import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# Maximum request size (10MB)
MAX_REQUEST_SIZE = 10 * 1024 * 1024


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for request validation and sanitization."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Validate and sanitize requests."""
        # Check request size
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                size = int(content_length)
                if size > MAX_REQUEST_SIZE:
                    return JSONResponse(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        content={
                            "error": {
                                "message": "Request entity too large",
                                "status_code": 413,
                                "error_code": "ERR_413",
                                "details": {
                                    "max_size": MAX_REQUEST_SIZE,
                                    "requested_size": size,
                                },
                            }
                        },
                    )
            except ValueError:
                # Invalid content-length header, continue
                pass

        # Validate content type for POST/PUT/PATCH requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            allowed = (
                "application/json",
                "application/x-www-form-urlencoded",
                "multipart/form-data",
            )
            if (
                not content_type.startswith(allowed)
                and content_length
                and int(content_length) > 0
            ):
                # Allow empty content type (some clients don't send it)
                logger.warning(
                    f"Unexpected content-type: {content_type} for "
                    f"{request.method} {request.url.path}"
                )

        return await call_next(request)
