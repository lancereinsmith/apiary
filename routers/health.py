"""Health check endpoints."""

import time
from typing import Any

import fastapi
from fastapi import Depends
from pydantic import BaseModel

from __version__ import __version__
from config import Settings, get_settings


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
) -> HealthDetail:
    """Readiness probe with dependency health checks.

    Checks configuration validity and reports registered services.
    External service health is not checked here to avoid coupling
    the readiness probe to specific service implementations.
    """
    dependencies: dict[str, Any] = {}
    overall_status = "ready"

    # Check configuration
    try:
        _ = settings.api_keys
        dependencies["configuration"] = {"status": "healthy"}
    except Exception as e:
        dependencies["configuration"] = {
            "status": "unhealthy",
            "error": str(e),
        }
        overall_status = "unready"

    # Report registered services (informational, not a health gate)
    from core.services import list_services

    registered = list_services()
    dependencies["services"] = {
        "status": "healthy",
        "registered": registered,
        "count": len(registered),
    }

    uptime = time.time() - _start_time

    return HealthDetail(
        status=overall_status,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        version=__version__,
        uptime_seconds=uptime,
        dependencies=dependencies,
    )
