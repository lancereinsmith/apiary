"""Shared dependencies for dependency injection."""

from functools import lru_cache

import httpx

from config import Settings, get_settings


@lru_cache
def get_settings_cached() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance (cached).
    """
    return get_settings()


def get_http_client() -> httpx.AsyncClient:
    """Get an HTTP client instance.

    Note: This creates a new client each time. For connection pooling,
    consider using a shared client instance managed by the application.

    Returns:
        httpx.AsyncClient instance.
    """
    return httpx.AsyncClient(timeout=30.0, follow_redirects=True)


class HTTPClientDependency:
    """Dependency class for HTTP client with connection pooling."""

    def __init__(self):
        """Initialize the HTTP client dependency."""
        self._client: httpx.AsyncClient | None = None

    async def __call__(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
            )
        return self._client

    async def close(self):
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None


# Global HTTP client dependency instance
http_client_dependency = HTTPClientDependency()
