"""Endpoint configuration models and validation."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class HTTPMethod(str, Enum):
    """HTTP methods supported by endpoints."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class EndpointConfig(BaseModel):
    """Configuration for a single endpoint."""

    path: str = Field(..., description="Endpoint path (e.g., '/api/custom')")
    method: HTTPMethod = Field(default=HTTPMethod.GET, description="HTTP method")
    service: str = Field(..., description="Service name to call")
    enabled: bool = Field(default=True, description="Whether endpoint is enabled")
    requires_auth: bool = Field(
        default=False, description="Whether endpoint requires authentication"
    )
    description: Optional[str] = Field(
        None, description="Endpoint description for API docs"
    )
    tags: List[str] = Field(default_factory=list, description="OpenAPI tags")
    parameters: Optional[Dict[str, Any]] = Field(
        None, description="Service parameters mapping"
    )
    response_model: Optional[str] = Field(
        None, description="Response model name (optional)"
    )
    summary: Optional[str] = Field(None, description="Endpoint summary for API docs")

    @field_validator("path")
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Validate endpoint path."""
        if not v.startswith("/"):
            raise ValueError("Path must start with '/'")
        return v


class EndpointsConfig(BaseModel):
    """Configuration for all endpoints."""

    endpoints: List[EndpointConfig] = Field(
        default_factory=list, description="List of endpoint configurations"
    )

    @field_validator("endpoints")
    @classmethod
    def validate_endpoints(cls, v: List[EndpointConfig]) -> List[EndpointConfig]:
        """Validate endpoints for duplicates."""
        paths_methods = [(e.path, e.method) for e in v if e.enabled]
        if len(paths_methods) != len(set(paths_methods)):
            duplicates = [
                (p, m) for p, m in paths_methods if paths_methods.count((p, m)) > 1
            ]
            raise ValueError(f"Duplicate endpoint definitions: {duplicates}")
        return v


def load_endpoints_config(file_path: str = "config/endpoints.json") -> EndpointsConfig:
    """Load endpoints configuration from JSON file.

    Args:
        file_path: Path to endpoints configuration file

    Returns:
        EndpointsConfig instance

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config is invalid
    """
    import json
    from pathlib import Path

    config_path = Path(file_path)
    if not config_path.exists():
        # Return empty config if file doesn't exist
        return EndpointsConfig()

    with open(config_path, "r") as f:
        data = json.load(f)

    return EndpointsConfig(**data)
