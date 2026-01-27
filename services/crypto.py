"""Cryptocurrency price service using CoinLore API.

This module provides functionality to fetch real-time cryptocurrency price data
from the CoinLore API (https://api.coinlore.net/api/tickers/). It supports
querying any cryptocurrency by its symbol (e.g., BTC, ETH, SOL).

The API returns comprehensive market data including:
- Current price in USD and BTC
- Market capitalization and volume
- Price change percentages (1h, 24h, 7d)
- Supply information (circulating, total, max)
"""

from typing import Any

import httpx

from core import ValidationError

# CoinLore API endpoint for cryptocurrency ticker data
URL = "https://api.coinlore.net/api/tickers/"


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float.

    Handles None, empty strings, and invalid values gracefully.

    Args:
        value: Value to convert (can be string, number, None, etc.)
        default: Default value to return if conversion fails

    Returns:
        Float value or default if conversion fails
    """
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    """Safely convert a value to int.

    Handles None, empty strings, and invalid values gracefully.
    First converts to float to handle string numbers, then to int.

    Args:
        value: Value to convert (can be string, number, None, etc.)
        default: Default value to return if conversion fails

    Returns:
        Integer value or default if conversion fails
    """
    if value is None or value == "":
        return default
    try:
        # Convert via float first to handle string numbers like "1.00"
        return int(float(value))
    except (ValueError, TypeError):
        return default


async def get_price_data(
    symbol: str = "BTC", client: httpx.AsyncClient | None = None
) -> dict:
    """Get cryptocurrency price data by symbol from CoinLore API.

    Fetches real-time market data for the specified cryptocurrency symbol.
    The search is case-insensitive, so "btc", "BTC", and "Btc" all work.

    Args:
        symbol: Cryptocurrency symbol (e.g., "BTC", "ETH", "SOL", "DOGE").
                Defaults to "BTC" if not provided.
        client: Optional HTTP client. If not provided, creates a new one
                and manages its lifecycle.

    Returns:
        Dictionary containing cryptocurrency market data with the following keys:
        - symbol (str): Cryptocurrency symbol (e.g., "BTC")
        - name (str): Full name of the cryptocurrency (e.g., "Bitcoin")
        - rank (int): Market capitalization rank (1 = highest)
        - price_usd (float): Current price in USD
        - percent_change_24h (float): 24-hour price change percentage
        - percent_change_1h (float): 1-hour price change percentage
        - percent_change_7d (float): 7-day price change percentage
        - market_cap_usd (float): Market capitalization in USD
        - volume24 (float): 24-hour trading volume
        - price_btc (float): Current price in BTC
        - csupply (str): Circulating supply
        - tsupply (str): Total supply
        - msupply (str): Maximum supply (may be None or empty)

    Raises:
        ValidationError: If the API request fails (non-200 status) or if the
                        specified symbol is not found in the API response.

    Example:
        >>> import httpx
        >>> client = httpx.AsyncClient()
        >>> data = await get_price_data("BTC", client)
        >>> print(data["price_usd"])
        87555.25
        >>> await client.aclose()
    """
    use_provided_client = client is not None

    if not use_provided_client:
        client = httpx.AsyncClient(timeout=30.0)

    assert (
        client is not None
    )  # type narrow: client is set above when use_provided_client is False
    try:
        # Fetch ticker data from CoinLore API
        resp: httpx.Response = await client.get(URL)
        if resp.status_code != 200:
            raise ValidationError(
                f"Failed to fetch cryptocurrency data from CoinLore API: "
                f"HTTP {resp.status_code} - {resp.text}",
                status_code=resp.status_code,
            )

        # Parse JSON response
        respjson = resp.json()
        data = respjson.get("data", [])

        if not data:
            raise ValidationError(
                "CoinLore API returned empty data",
                status_code=500,
            )

        # Find the coin by symbol (case-insensitive search)
        symbol_upper = symbol.upper()
        coin_data = None
        for coin in data:
            if coin.get("symbol", "").upper() == symbol_upper:
                coin_data = coin
                break

        if coin_data is None:
            raise ValidationError(
                f"Symbol '{symbol}' not found in cryptocurrency data. "
                f"Please check the symbol and try again.",
                status_code=404,
            )

        # Extract and return relevant fields with safe type conversion
        return {
            "symbol": coin_data.get("symbol"),
            "name": coin_data.get("name"),
            "rank": _safe_int(coin_data.get("rank"), 0),
            "price_usd": _safe_float(coin_data.get("price_usd"), 0.0),
            "percent_change_24h": _safe_float(coin_data.get("percent_change_24h"), 0.0),
            "percent_change_1h": _safe_float(coin_data.get("percent_change_1h"), 0.0),
            "percent_change_7d": _safe_float(coin_data.get("percent_change_7d"), 0.0),
            "market_cap_usd": _safe_float(coin_data.get("market_cap_usd"), 0.0),
            "volume24": _safe_float(coin_data.get("volume24"), 0.0),
            "price_btc": _safe_float(coin_data.get("price_btc"), 0.0),
            "csupply": coin_data.get("csupply"),
            "tsupply": coin_data.get("tsupply"),
            "msupply": coin_data.get("msupply"),
        }
    finally:
        # Clean up HTTP client if we created it
        if not use_provided_client:
            await client.aclose()
