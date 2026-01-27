"""Pytest configuration and shared fixtures."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app import api
from config import Settings


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(api)


@pytest.fixture
async def async_client():
    """Create an async test client for the FastAPI app."""
    from httpx import ASGITransport

    transport = ASGITransport(app=api)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    return Settings(
        api_keys="test-api-key-1,test-api-key-2",
    )


@pytest.fixture
def mock_http_client():
    """Create a mock HTTP client."""
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"test": "data"}
    mock_response.text = '{"test": "data"}'
    mock_client.get.return_value = mock_response
    mock_client.post.return_value = mock_response
    return mock_client


@pytest.fixture
def auth_headers():
    """Create authentication headers for testing."""
    return {"X-API-Key": "test-api-key-1"}


@pytest.fixture
def no_auth_headers():
    """Create headers without authentication."""
    return {}
