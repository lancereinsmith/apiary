"""Health check endpoints."""

import time
from typing import Any

import fastapi
import httpx
from fastapi import Depends
from pydantic import BaseModel

from __version__ import __version__
from config import Settings, get_settings
from core.dependencies import http_client_dependency


class HealthStatus(BaseModel):
    """Health status response model."""

    status: str
    timestamp: str
    version: str = __version__


class HealthDetail(BaseModel):
    """Detailed health check response."""

    status: str
    timestamp: str
    version: str
    uptime_seconds: float
    dependencies: dict[str, Any]


router = fastapi.APIRouter(tags=["health"])

# Track application start time
_start_time = time.time()


@router.get(
    "/health",
    response_model=HealthStatus,
    summary="Health check",
    description="Returns the health status of the API",
)
async def health_check() -> HealthStatus:
    """Basic health check endpoint."""
    return HealthStatus(
        status="healthy",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )


@router.get(
    "/health/live",
    response_model=HealthStatus,
    summary="Liveness probe",
    description="Kubernetes liveness probe endpoint",
)
async def liveness() -> HealthStatus:
    """Liveness probe for container orchestration."""
    return HealthStatus(
        status="alive",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )


@router.get(
    "/health/ready",
    response_model=HealthDetail,
    summary="Readiness probe",
    description="Kubernetes readiness probe with dependency checks",
)
async def readiness(
    settings: Settings = Depends(get_settings),
    client: httpx.AsyncClient = Depends(http_client_dependency),
) -> HealthDetail:
    """Readiness probe with dependency health checks."""
    dependencies: dict[str, Any] = {}
    overall_status = "ready"

    # Check external API dependencies
    try:
        # Check CoinLore Crypto API
        resp = await client.get(
            "https://api.coinlore.net/api/tickers/",
            timeout=5.0,
        )
        dependencies["crypto_api"] = {
            "status": "healthy" if resp.status_code == 200 else "unhealthy",
            "status_code": resp.status_code,
        }
        if resp.status_code != 200:
            overall_status = "degraded"
    except Exception as e:
        dependencies["crypto_api"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        overall_status = "degraded"

    # Check configuration
    try:
        # Verify settings are loaded correctly
        _ = settings.api_keys
        dependencies["configuration"] = {"status": "healthy"}
    except Exception as e:
        dependencies["configuration"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        overall_status = "unready"

    uptime = time.time() - _start_time

    return HealthDetail(
        status=overall_status,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        version=__version__,
        uptime_seconds=uptime,
        dependencies=dependencies,
    )
