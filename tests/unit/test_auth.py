"""Unit tests for authentication."""

import pytest

from config import Settings
from core import AuthenticationError
from core.auth.authentication import validate_api_key, verify_api_key


def test_validate_api_key_valid():
    """Test API key validation with valid key."""
    settings = Settings(api_keys="key1,key2,key3")
    assert validate_api_key("key1", settings) is True
    assert validate_api_key("key2", settings) is True
    assert validate_api_key("key3", settings) is True


def test_validate_api_key_invalid():
    """Test API key validation with invalid key."""
    settings = Settings(api_keys="key1,key2")
    assert validate_api_key("invalid", settings) is False


def test_validate_api_key_empty():
    """Test API key validation with empty keys."""
    settings = Settings(api_keys="")
    assert validate_api_key("any-key", settings) is False


def test_validate_api_key_whitespace():
    """Test API key validation handles whitespace."""
    settings = Settings(api_keys=" key1 , key2 ")
    assert validate_api_key("key1", settings) is True
    assert validate_api_key("key2", settings) is True


@pytest.mark.asyncio
async def test_verify_api_key_missing():
    """Test verify_api_key raises error when key is missing."""
    with pytest.raises(AuthenticationError) as exc_info:
        await verify_api_key(api_key=None, settings=Settings(api_keys="key1"))
    assert "API key required" in exc_info.value.message


@pytest.mark.asyncio
async def test_verify_api_key_invalid():
    """Test verify_api_key raises error when key is invalid."""
    settings = Settings(api_keys="key1")
    with pytest.raises(AuthenticationError) as exc_info:
        await verify_api_key(api_key="invalid", settings=settings)
    assert "Invalid API key" in exc_info.value.message


@pytest.mark.asyncio
async def test_verify_api_key_valid():
    """Test verify_api_key returns key when valid."""
    settings = Settings(api_keys="key1")
    result = await verify_api_key(api_key="key1", settings=settings)
    assert result == "key1"
