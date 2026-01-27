"""Response models for API endpoints."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Base response model."""

    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Response timestamp",
    )


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: dict[str, Any] = Field(..., description="Error details")


class BaseDataResponse(BaseResponse):
    """Base response for data endpoints."""

    datetime: str = Field(..., description="Current datetime in ISO format")


class CryptoPriceResponse(BaseDataResponse):
    """Response model for cryptocurrency price endpoint."""

    symbol: str = Field(..., description="Cryptocurrency symbol (e.g., BTC, ETH)")
    name: str = Field(..., description="Full name of the cryptocurrency")
    rank: int = Field(..., description="Market capitalization rank", ge=1)
    price_usd: float = Field(..., description="Price in USD", ge=0)
    percent_change_24h: float = Field(
        ..., description="24-hour price change percentage"
    )
    percent_change_1h: float = Field(..., description="1-hour price change percentage")
    percent_change_7d: float = Field(..., description="7-day price change percentage")
    market_cap_usd: float = Field(..., description="Market capitalization in USD", ge=0)
    volume24: float = Field(..., description="24-hour trading volume", ge=0)
    price_btc: float = Field(..., description="Price in BTC", ge=0)
    csupply: str = Field(default="", description="Circulating supply")
    tsupply: str = Field(default="", description="Total supply")
    msupply: str = Field(default="", description="Maximum supply")


class BaseCombinedResponse(BaseDataResponse):
    """Base response for combined data endpoints."""

    pass


# Example responses for OpenAPI documentation
EXAMPLE_CRYPTO = {
    "datetime": "2024-01-01T12:00:00",
    "timestamp": "2024-01-01T12:00:00",
    "symbol": "BTC",
    "name": "Bitcoin",
    "rank": 1,
    "price_usd": 87555.25,
    "percent_change_24h": -0.22,
    "percent_change_1h": -0.12,
    "percent_change_7d": -1.41,
    "market_cap_usd": 1745467256544.10,
    "volume24": 16800053792.03,
    "price_btc": 1.00,
    "csupply": "19961774.00",
    "tsupply": "19961774",
    "msupply": "21000000",
}
