"""Caching utilities for endpoints."""

import hashlib
import json
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from fastapi import Response


class SimpleCache:
    """Simple in-memory cache with TTL."""

    def __init__(self):
        """Initialize cache."""
        self._cache: dict[str, tuple[Any, float]] = {}
        self._cleanup_interval = 60  # Clean up every 60 seconds
        self._last_cleanup = time.time()

    def _cleanup_expired(self):
        """Remove expired cache entries."""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return

        expired_keys = [
            key for key, (_, expiry) in self._cache.items() if expiry < current_time
        ]
        for key in expired_keys:
            del self._cache[key]

        self._last_cleanup = current_time

    def get(self, key: str) -> Any | None:
        """Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        self._cleanup_expired()

        if key not in self._cache:
            return None

        value, expiry = self._cache[key]
        if time.time() > expiry:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl: int = 60):
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
        """
        self._cleanup_expired()
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)

    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()


# Global cache instance
_cache = SimpleCache()


def cache_response(ttl: int = 60, key_func: Callable | None = None):
    """Decorator to cache endpoint responses.

    Args:
        ttl: Time to live in seconds
        key_func: Optional function to generate cache key from request

    Returns:
        Decorated function
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default: use function name and arguments
                key_data = {
                    "func": getattr(func, "__name__", "unknown"),
                    "args": str(args),
                    "kwargs": str(sorted(kwargs.items())),
                }
                cache_key = hashlib.md5(
                    json.dumps(key_data, sort_keys=True).encode()
                ).hexdigest()

            # Check cache
            cached = _cache.get(cache_key)
            if cached is not None:
                return cached

            # Call function
            result = await func(*args, **kwargs)

            # Cache result
            _cache.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator


def add_cache_headers(response: Response, ttl: int = 60, etag: str | None = None):
    """Add cache headers to response.

    Args:
        response: FastAPI response object
        ttl: Time to live in seconds
        etag: Optional ETag value
    """
    response.headers["Cache-Control"] = f"public, max-age={ttl}"
    if etag:
        response.headers["ETag"] = etag
