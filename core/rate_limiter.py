"""Rate limiting middleware and utilities."""

import time
from collections import defaultdict

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from config import get_settings


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self):
        """Initialize rate limiter."""
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._cleanup_interval = 60  # Clean up old entries every 60 seconds
        self._last_cleanup = time.time()

    def _cleanup_old_entries(self):
        """Remove entries older than 1 minute."""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return

        cutoff_time = current_time - 60
        for key in list(self._requests.keys()):
            self._requests[key] = [
                timestamp
                for timestamp in self._requests[key]
                if timestamp > cutoff_time
            ]
            if not self._requests[key]:
                del self._requests[key]

        self._last_cleanup = current_time

    def check_rate_limit(
        self, identifier: str, limit: int, window_seconds: int = 60
    ) -> tuple[bool, int, int]:
        """Check if request is within rate limit.

        Args:
            identifier: Unique identifier (IP address, API key, etc.)
            limit: Maximum number of requests allowed
            window_seconds: Time window in seconds (default: 60)

        Returns:
            Tuple of (is_allowed, remaining, reset_time)
        """
        self._cleanup_old_entries()

        current_time = time.time()
        cutoff_time = current_time - window_seconds

        # Get requests in the current window
        requests = [ts for ts in self._requests[identifier] if ts > cutoff_time]
        self._requests[identifier] = requests

        # Check if limit exceeded
        if len(requests) >= limit:
            reset_time = int(requests[0] + window_seconds)
            return False, 0, reset_time

        # Add current request
        requests.append(current_time)
        self._requests[identifier] = requests

        remaining = max(0, limit - len(requests))
        reset_time = int(current_time + window_seconds)

        return True, remaining, reset_time


# Global rate limiter instance
_rate_limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """Apply rate limiting to requests."""
        settings = get_settings()

        # Skip rate limiting if disabled
        if not settings.rate_limit_enabled:
            return await call_next(request)

        # Determine identifier (IP address or API key)
        identifier = request.client.host if request.client else "unknown"
        api_key = request.headers.get("X-API-Key")
        is_authenticated = bool(api_key)

        # Use API key as identifier if authenticated
        if is_authenticated:
            identifier = f"api_key:{api_key}"

        # Determine rate limit
        if is_authenticated:
            limit = settings.rate_limit_per_minute_authenticated
        else:
            limit = settings.rate_limit_per_minute

        # Check rate limit
        allowed, remaining, reset_time = _rate_limiter.check_rate_limit(
            identifier, limit
        )

        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_time)

        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": {
                        "message": "Rate limit exceeded",
                        "status_code": 429,
                        "details": {
                            "limit": limit,
                            "reset_time": reset_time,
                        },
                    }
                },
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time),
                },
            )

        return response
