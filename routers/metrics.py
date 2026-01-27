"""Metrics endpoint."""

import fastapi
from pydantic import BaseModel

from core.metrics import metrics_collector

router = fastapi.APIRouter(tags=["metrics"])


class MetricsResponse(BaseModel):
    """Metrics response model."""

    uptime_seconds: float
    total_requests: int
    total_errors: int
    error_rate: float
    endpoints: dict


@router.get(
    "/metrics",
    response_model=MetricsResponse,
    summary="Application metrics",
    description=(
        "Returns application metrics including request counts, "
        "error rates, and endpoint statistics"
    ),
    responses={
        200: {
            "description": "Metrics data",
            "content": {
                "application/json": {
                    "example": {
                        "uptime_seconds": 3600.0,
                        "total_requests": 1000,
                        "total_errors": 10,
                        "error_rate": 0.01,
                        "endpoints": {
                            "GET /health": {
                                "count": 100,
                                "average_time": 0.001,
                                "error_count": 0,
                                "error_rate": 0.0,
                                "status_codes": {"200": 100},
                            }
                        },
                    }
                }
            },
        }
    },
)
async def get_metrics() -> MetricsResponse:
    """Get application metrics.

    Returns:
        MetricsResponse with application metrics
    """
    metrics = metrics_collector.get_metrics()
    return MetricsResponse(**metrics)
