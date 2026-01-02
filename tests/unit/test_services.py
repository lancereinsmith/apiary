"""Unit tests for services."""

from unittest.mock import MagicMock

import pytest

from core import ValidationError
from services.crypto_service import CryptoService


@pytest.mark.asyncio
async def test_crypto_service_success(mock_http_client):
    """Test Crypto service with successful response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "id": "90",
                "symbol": "BTC",
                "name": "Bitcoin",
                "rank": 1,
                "price_usd": "87555.25",
                "percent_change_24h": "-0.22",
                "percent_change_1h": "-0.12",
                "percent_change_7d": "-1.41",
                "price_btc": "1.00",
                "market_cap_usd": "1745467256544.10",
                "volume24": 16800053792.03,
                "csupply": "19961774.00",
                "tsupply": "19961774",
                "msupply": "21000000",
            }
        ],
        "info": {"coins_num": 14949, "time": 1766956563},
    }
    mock_http_client.get.return_value = mock_response

    service = CryptoService(http_client=mock_http_client)
    result = await service.call()

    assert "symbol" in result
    assert result["symbol"] == "BTC"
    assert result["name"] == "Bitcoin"
    assert result["price_usd"] == 87555.25
    assert result["rank"] == 1
    mock_http_client.get.assert_called_once()


@pytest.mark.asyncio
async def test_crypto_service_with_symbol_parameter(mock_http_client):
    """Test Crypto service with symbol parameter."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "id": "80",
                "symbol": "ETH",
                "name": "Ethereum",
                "rank": 2,
                "price_usd": "2930.67",
                "percent_change_24h": "-0.04",
                "percent_change_1h": "-0.22",
                "percent_change_7d": "-2.12",
                "price_btc": "0.033470",
                "market_cap_usd": "353743182917.02",
                "volume24": 7319824035.78,
                "csupply": "120703849.62",
                "tsupply": "122375302",
                "msupply": "",
            }
        ],
        "info": {"coins_num": 14949, "time": 1766956563},
    }
    mock_http_client.get.return_value = mock_response

    service = CryptoService(http_client=mock_http_client)
    result = await service.call({"symbol": "ETH"})

    assert result["symbol"] == "ETH"
    assert result["name"] == "Ethereum"
    assert result["price_usd"] == 2930.67
    assert result["rank"] == 2


@pytest.mark.asyncio
async def test_crypto_service_symbol_not_found(mock_http_client):
    """Test Crypto service when symbol is not found."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "id": "90",
                "symbol": "BTC",
                "name": "Bitcoin",
                "rank": 1,
                "price_usd": "87555.25",
            }
        ],
        "info": {"coins_num": 14949, "time": 1766956563},
    }
    mock_http_client.get.return_value = mock_response

    service = CryptoService(http_client=mock_http_client)

    with pytest.raises(ValidationError) as exc_info:
        await service.call({"symbol": "INVALID"})
    assert "not found" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_crypto_service_failure(mock_http_client):
    """Test Crypto service with failed API response."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_http_client.get.return_value = mock_response

    service = CryptoService(http_client=mock_http_client)

    with pytest.raises(ValidationError):
        await service.call()
