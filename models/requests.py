"""Request models for API endpoints."""

from pydantic import BaseModel, Field


class HealthCheckQuery(BaseModel):
    """Query parameters for health check endpoints."""

    detailed: bool = Field(
        default=False, description="Return detailed health information"
    )
