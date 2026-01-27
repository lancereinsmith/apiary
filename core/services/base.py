"""Base service interface for extensible services."""

from abc import ABC, abstractmethod
from typing import Any

import httpx


class BaseService(ABC):
    """Base class for all services."""

    def __init__(self, http_client: httpx.AsyncClient | None = None):
        """Initialize service.

        Args:
            http_client: Optional HTTP client (will create one if not provided)
        """
        self._http_client = http_client
        self._owns_client = http_client is None

    @property
    def name(self) -> str:
        """Get service name."""
        return self.__class__.__name__.lower().replace("service", "")

    @abstractmethod
    async def call(self, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        """Call the service with given parameters.

        Args:
            parameters: Service parameters

        Returns:
            Service response as dictionary

        Raises:
            Exception: If service call fails
        """
        pass

    async def get_http_client(self) -> httpx.AsyncClient:
        """Get HTTP client (creates one if needed).

        Returns:
            httpx.AsyncClient instance
        """
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(timeout=30.0)
        return self._http_client

    async def cleanup(self):
        """Cleanup resources."""
        if self._owns_client and self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

    def __del__(self) -> None:  # noqa: B027
        """Cleanup on deletion."""
        # Note: This is a fallback, proper cleanup should use async context manager
        pass
