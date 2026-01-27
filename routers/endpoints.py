"""Endpoint discovery and management."""

import fastapi
from pydantic import BaseModel

from config.endpoint_config import load_endpoints_config
from core.services import list_services

router = fastapi.APIRouter(tags=["endpoints"])


class EndpointInfo(BaseModel):
    """Information about an endpoint."""

    path: str
    method: str
    service: str
    enabled: bool
    requires_auth: bool
    description: str | None
    tags: list[str]
    summary: str | None


class EndpointsInfoResponse(BaseModel):
    """Response model for endpoints discovery."""

    endpoints: list[EndpointInfo]
    services: list[str]
    total: int


@router.get(
    "/endpoints",
    response_model=EndpointsInfoResponse,
    summary="List configurable endpoints",
    description="Discover all configurable endpoints and available services",
)
async def list_endpoints() -> EndpointsInfoResponse:
    """List all configurable endpoints.

    Returns:
        EndpointsInfoResponse with endpoint information
    """
    try:
        config = load_endpoints_config()
        endpoints = [
            EndpointInfo(
                path=e.path,
                method=e.method.value,
                service=e.service,
                enabled=e.enabled,
                requires_auth=e.requires_auth,
                description=e.description,
                tags=e.tags,
                summary=e.summary,
            )
            for e in config.endpoints
        ]
    except Exception:
        endpoints = []

    services = list_services()

    return EndpointsInfoResponse(
        endpoints=endpoints,
        services=services,
        total=len(endpoints),
    )
