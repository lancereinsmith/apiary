# Adding Endpoints

This guide explains how to add new endpoints to your Apiary API using both code-based and configuration-based approaches.

## Overview

Apiary supports two methods for creating endpoints:

1. **Configuration-based** - JSON configuration for rapid development
2. **Code-based** - Traditional FastAPI approach with full control

## When to Use Each Approach

### Use **Configuration-Based** Endpoints When

- Simple service call
- Rapid prototyping
- Enable/disable without deployment
- Standard request/response pattern
- Non-technical configuration

### Use **Code-Based** Endpoints When

- Complex business logic required
- Custom validation needed
- Special error handling
- Multiple service orchestration
- Custom response formatting

## Configuration-Based Endpoints

Configuration-based endpoints allow you to add endpoints without writing code.

### Step 1: Create a Service

If you need a new service, create it in `services_custom/` (or `services/` for in-repo only).
Use `services_custom/` so it is not overwritten when you pull updates.

```python
# services_custom/example_service.py
"""Example service."""

from typing import Any, Dict, Optional
from core.services.base import BaseService

class ExampleService(BaseService):
    """Example service for demonstration."""

    service_name = "example"  # Service registration name

    async def call(
        self, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute the service.

        Args:
            parameters: Request parameters

        Returns:
            Service response
        """
        parameters = parameters or {}
        name = parameters.get("name", "World")

        return {
            "message": f"Hello, {name}!",
            "timestamp": self._get_timestamp(),
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### Step 2: Add Endpoint Configuration

Edit `config/endpoints.json`:

```json
{
  "endpoints": [
    {
      "path": "/api/example",
      "method": "GET",
      "service": "example",
      "enabled": true,
      "requires_auth": false,
      "description": "Example endpoint",
      "tags": ["example"],
      "summary": "Get example data"
    }
  ]
}
```

### Step 3: Restart Server

Restart the server to load the new endpoint:

```bash
uv run apiary serve --reload
```

Test your endpoint:

```bash
curl http://localhost:8000/api/example
```

### Configuration Options

Basic fields for endpoint configuration:

| Field | Required | Description |
|-------|----------|-------------|
| `path` | Yes | Endpoint path (e.g., `/api/example`) |
| `method` | Yes | HTTP method (GET, POST, PUT, DELETE, PATCH) |
| `service` | Yes | Service name to call |
| `enabled` | No | Enable/disable endpoint (default: true) |
| `requires_auth` | No | Require authentication (default: false) |
| `description` | No | Full description for API docs |
| `tags` | No | OpenAPI tags for grouping |
| `summary` | No | Brief summary |
| `parameters` | No | Parameter mapping (see below) |

For advanced options like endpoint-specific API keys, see [Advanced Endpoint Patterns](advanced-endpoints.md).

## Parameter Mapping

Configuration-based endpoints support parameter mapping.

### Query Parameters

Map query parameters to service parameters:

```json
{
  "path": "/api/greet",
  "method": "GET",
  "service": "greet",
  "enabled": true,
  "requires_auth": false,
  "parameters": {
    "name": {
      "source": "query",
      "key": "name"
    }
  }
}
```

Usage: `GET /api/greet?name=Alice`

### Path Parameters

Map path parameters:

```json
{
  "path": "/api/user/{id}",
  "method": "GET",
  "service": "user",
  "enabled": true,
  "requires_auth": false,
  "parameters": {
    "user_id": {
      "source": "path",
      "key": "id"
    }
  }
}
```

Usage: `GET /api/user/123`

### Static Values

Provide static values to services:

```json
{
  "path": "/api/example",
  "method": "GET",
  "service": "example",
  "enabled": true,
  "requires_auth": false,
  "parameters": {
    "version": "v1",
    "source": "api"
  }
}
```

!!! tip "Advanced Parameter Mapping"
    For mixed parameters and complex configurations, see [Advanced Endpoint Patterns](advanced-endpoints.md).

## Complete Example: Weather Service

Create `services_custom/weather_service.py` (or `services/` for in-repo only):

```python
from typing import Any, Dict, Optional
from core.services.base import BaseService
from core import ValidationError
import httpx

class WeatherService(BaseService):
    """Weather data service."""

    async def call(
        self, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get weather data.

        Args:
            parameters: Must include 'city'

        Returns:
            Weather data
        """
        parameters = parameters or {}
        city = parameters.get("city")

        if not city:
            raise ValidationError("City parameter required")

        # Call weather API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.weatherapi.com/v1/current.json",
                params={"q": city, "key": "YOUR_API_KEY"}
            )

            if response.status_code != 200:
                raise ValidationError("Failed to fetch weather data")

            data = response.json()

            return {
                "city": city,
                "temperature": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
            }
```

Configure endpoint:

```json
{
  "path": "/api/weather",
  "method": "GET",
  "service": "weather",
  "enabled": true,
  "requires_auth": false,
  "description": "Get current weather for a city",
  "tags": ["weather"],
  "parameters": {
    "city": {
      "source": "query",
      "key": "city"
    }
  }
}
```

Usage: `GET /api/weather?city=London`

!!! tip "More Examples"
    For advanced examples including admin endpoints, multi-tier access, and partner integrations, see [Advanced Endpoint Patterns](advanced-endpoints.md).

## Code-Based Endpoints

### Basic Endpoint

Create a simple endpoint in a router file in `routers_custom/` (e.g. `routers_custom/example.py`):

```python
"""Example router."""

import fastapi

router = fastapi.APIRouter(tags=["example"])

@router.get("/hello")
async def hello():
    """Simple hello endpoint."""
    return {"message": "Hello, World!"}
```

### Endpoint with Dependencies

Use dependency injection for HTTP clients, settings, etc.:

```python
from fastapi import Depends
import httpx
from core.dependencies import http_client_dependency
from config import Settings, get_settings

@router.get("/data")
async def get_data(
    client: httpx.AsyncClient = Depends(http_client_dependency),
    settings: Settings = Depends(get_settings),
):
    """Fetch data from external API."""
    response = await client.get("https://api.example.com/data")
    return response.json()
```

### Endpoint with Query Parameters

```python
from fastapi import Depends
from pydantic import BaseModel

class QueryParams(BaseModel):
    """Query parameters model."""
    name: str
    count: int = 10

@router.get("/greet")
async def greet(params: QueryParams = Depends()):
    """Greet endpoint with query parameters."""
    return {
        "message": f"Hello, {params.name}!",
        "count": params.count,
    }
```

Usage: `GET /greet?name=Alice&count=5`

### Protected Endpoint

Require authentication using the `require_auth` dependency:

```python
from core.auth.authorization import require_auth
from core.auth.authentication import AuthenticatedUser

@router.get("/protected")
async def protected_endpoint(
    user: AuthenticatedUser = Depends(require_auth),
):
    """Protected endpoint requiring API key."""
    return {
        "message": "You are authenticated",
        "api_key": user.api_key,
    }
```

!!! info "API Key Configuration"
    Protected endpoints use the global API keys configured in `config/settings.json`.
    For endpoint-specific keys, see [Advanced Endpoint Patterns](advanced-endpoints.md).

### Response Models

Define response models for better documentation and validation:

```python
from pydantic import BaseModel
from models.responses import BaseResponse

class DataResponse(BaseResponse):
    """Response model for data endpoint."""
    data: dict
    count: int

@router.get("/data", response_model=DataResponse)
async def get_data() -> DataResponse:
    """Get data with typed response."""
    return DataResponse(
        data={"key": "value"},
        count=1,
    )
```

### Error Handling

Use custom exceptions from `core.exceptions`:

```python
from core import ValidationError, NotFoundError

@router.get("/user/{user_id}")
async def get_user(user_id: int):
    """Get user by ID."""
    user = await fetch_user(user_id)

    if not user:
        raise NotFoundError(f"User {user_id} not found")

    if not user.is_active:
        raise ValidationError("User is not active")

    return user
```

### Caching

Add cache headers to reduce external API calls:

```python
from core.cache import add_cache_headers
from fastapi import Response

@router.get("/cached")
async def cached_endpoint(response: Response):
    """Endpoint with caching."""
    data = await expensive_operation()

    # Cache for 60 seconds
    add_cache_headers(response, ttl=60)

    return data
```

### Register Router

Routers are **automatically discovered** from `routers/` and `routers_custom/`. Put
custom routers in **`routers_custom/`** (gitignored, never overwritten by `git pull`);
use `routers/` only for in-repo development.

Save your router file (e.g., `routers_custom/example.py`) and add its name to
`config/settings.json`:

```json
{
  "enabled_routers": ["health", "metrics", "auth", "endpoints", "example"]
}
```

That's it!

!!! important "Use routers_custom/ for Deployments"
    Put custom routers in **`routers_custom/`**, not `routers/`. The `routers_custom/`
    directory is gitignored so your code is never overwritten when you pull updates.
    Run `uv run apiary init` to create it.

!!! info "How Auto-Discovery Works"
    The application scans `routers/` (built-in) and `routers_custom/` (your code) for
    Python files with a `router` attribute (APIRouter). You enable routers via
    `enabled_routers` in `config/settings.json`.

!!! tip "Consider Configuration-Based Endpoints"
    If your endpoint only needs to call a service and doesn't require complex custom logic, consider using [Configuration-Based Endpoints](#configuration-based-endpoints) instead. You can add endpoints via `config/endpoints.json` without any code changes.

## Troubleshooting

### Endpoint Not Appearing

**Configuration-based:**

- Check JSON syntax: `python -m json.tool config/endpoints.json`
- Verify service file exists in `services/` or `services_custom/`
- Ensure `enabled: true` in endpoint configuration
- Check logs for service discovery or registration errors

**Code-based:**

- Verify router file is in `routers/` or `routers_custom/` (use `routers_custom/` for custom code)
- Ensure the file exports a `router` variable (APIRouter instance)
- Check that router name is in `enabled_routers` in `config/settings.json`
- Check logs for import errors

### Authentication Not Working

- Verify `api_keys` in `config/settings.json`
- Check `requires_auth` setting is correct
- Ensure `X-API-Key` header is sent in requests
- Check logs for authentication errors
- For endpoint-specific keys, see [Advanced Endpoint Patterns](advanced-endpoints.md)

### Parameters Not Working

- Verify parameter mapping syntax in configuration
- Check parameter source (query/path) matches request
- Ensure parameter keys match exactly

## Next Steps

Ready for more advanced patterns?

- **[Advanced Endpoint Patterns](advanced-endpoints.md)** - Endpoint-specific API keys, multi-tier access, and more
- [Creating Services](creating-services.md) - Build robust services
- [Authentication](authentication.md) - Secure your endpoints
- [Built-in Endpoints](builtin-endpoints.md) - Use what's included
