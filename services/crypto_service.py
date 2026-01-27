"""Cryptocurrency price service with BaseService interface.

This module provides a BaseService implementation for fetching cryptocurrency
price data. It integrates with the core service architecture and can be
used in dynamic endpoint configurations.

The service accepts a 'symbol' parameter to query any cryptocurrency
supported by the CoinLore API.
"""

from typing import Any

from core.services.base import BaseService
from services.crypto import get_price_data


class CryptoService(BaseService):
    """Service for cryptocurrency price data using CoinLore API.

    This service provides access to real-time cryptocurrency market data
    through the CoinLore API. It implements the BaseService interface,
    making it compatible with the dynamic endpoint routing system.

    The service accepts an optional 'symbol' parameter in the parameters
    dictionary. If not provided, defaults to "BTC" (Bitcoin).

    Examples:
        Example usage in endpoint configuration:

        ```json
        {
            "path": "/api/crypto",
            "method": "GET",
            "service": "crypto",
            "parameters": {
                "symbol": "ETH"
            }
        }
        ```

        Using the service directly:

        ```python
        service = CryptoService()
        result = await service.call({"symbol": "ETH"})
        print(result["price_usd"])  # e.g., 2932.25
        await service.cleanup()
        ```
    """

    service_name = "crypto"

    async def call(self, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        """Get cryptocurrency price data by symbol.

        Retrieves comprehensive market data for the specified cryptocurrency
        symbol from the CoinLore API.

        Args:
            parameters: Optional service parameters dictionary containing:

                - symbol (str, optional): Cryptocurrency symbol to query
                  (e.g., "BTC", "ETH", "SOL", "DOGE"). Case-insensitive.
                  Defaults to "BTC" if not provided.

        Returns:
            Dictionary containing cryptocurrency market data with the following structure:

            ```python
            {
                "symbol": str,              # e.g., "BTC"
                "name": str,                 # e.g., "Bitcoin"
                "rank": int,                 # Market cap rank
                "price_usd": float,          # Price in USD
                "percent_change_24h": float, # 24h change %
                "percent_change_1h": float,  # 1h change %
                "percent_change_7d": float,  # 7d change %
                "market_cap_usd": float,     # Market cap in USD
                "volume24": float,          # 24h volume
                "price_btc": float,         # Price in BTC
                "csupply": str,              # Circulating supply
                "tsupply": str,              # Total supply
                "msupply": str               # Max supply (may be None)
            }
            ```

        Raises:
            ValidationError: If the API request fails or the symbol is not found.

        Examples:
            ```python
            service = CryptoService()
            result = await service.call({"symbol": "ETH"})
            print(result["price_usd"])  # e.g., 2932.25
            await service.cleanup()
            ```
        """
        # Extract symbol from parameters, defaulting to "BTC"
        symbol = "BTC"
        if parameters and "symbol" in parameters:
            symbol = str(parameters["symbol"]).strip()
            if not symbol:
                symbol = "BTC"  # Fallback to BTC if empty string provided

        # Get HTTP client from base class
        client = await self.get_http_client()

        # Fetch and return cryptocurrency data
        return await get_price_data(symbol=symbol, client=client)
