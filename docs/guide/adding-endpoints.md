# Adding Endpoints

This guide explains how to add new endpoints to your Apiary API using both code-based and configuration-based approaches.

## Overview

Apiary supports two methods for creating endpoints:

1. **Code-based** - Traditional FastAPI approach with full control
2. **Configuration-based** - JSON configuration for rapid development

## When to Use Each Approach

### Use Code-Based Endpoints When

- ✅ Complex business logic required
- ✅ Custom validation needed
- ✅ Special error handling
- ✅ Multiple service orchestration
- ✅ Custom response formatting

### Use Configuration-Based Endpoints When

- ✅ Simple service call
- ✅ Rapid prototyping
- ✅ Enable/disable without deployment
- ✅ Standard request/response pattern
- ✅ Non-technical configuration

## Code-Based Endpoints

### Basic Endpoint

Create a simple endpoint in a router file:

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

Add your router to `main.py`:

```python
from routers import example

def configure_routing():
    """Configure application routes."""
    api.include_router(example.router)
```

## Configuration-Based Endpoints

Configuration-based endpoints allow you to add endpoints without writing code.

### Step 1: Create a Service

If you need a new service, create it in `services/`:

```python
"""Example service."""

from typing import Any, Dict, Optional
from core.services.base import BaseService

class ExampleService(BaseService):
    """Example service for demonstration."""

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

### Step 2: Register Service

Register in `services/__init__.py`:

```python
from core.services import register_service
from services.example_service import ExampleService

register_service("example", ExampleService)
```

### Step 3: Add Endpoint Configuration

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

### Step 4: Test

Restart the server and test:

```bash
curl http://localhost:8000/api/example
```

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

Provide static values:

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

## Complete Examples

### Example 1: Weather Service

Create `services/weather_service.py`:

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

Register and configure:

```python
# services/__init__.py
register_service("weather", WeatherService)
```

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

### Example 2: Protected Admin Endpoint

Code-based approach:

```python
@router.get("/admin/stats")
async def admin_stats(
    user: AuthenticatedUser = Depends(require_auth),
):
    """Admin statistics endpoint."""
    return {
        "total_requests": get_total_requests(),
        "active_users": get_active_users(),
        "system_health": get_system_health(),
    }
```

Configuration-based approach:

```json
{
  "path": "/api/admin/stats",
  "method": "GET",
  "service": "admin_stats",
  "enabled": true,
  "requires_auth": true,
  "description": "Admin statistics (requires authentication)",
  "tags": ["admin"]
}
```

## Best Practices

### Code-Based Endpoints

1. **Use response models** for type safety
2. **Add comprehensive documentation** in docstrings
3. **Handle errors explicitly** with custom exceptions
4. **Use dependency injection** for testability
5. **Add cache headers** for expensive operations
6. **Log important events** for debugging

### Configuration-Based Endpoints

1. **Keep services simple** and focused
2. **Validate parameters** in service
3. **Use clear, descriptive paths**
4. **Document in configuration** (description, summary)
5. **Test thoroughly** after adding
6. **Version your APIs** if needed

### Both Approaches

1. **Test your endpoints** with unit and integration tests
2. **Monitor performance** using metrics
3. **Use semantic HTTP methods** (GET, POST, PUT, DELETE)
4. **Return appropriate status codes** (200, 400, 404, 500)
5. **Validate all input** before processing
6. **Document authentication requirements** clearly

## Troubleshooting

### Endpoint Not Appearing

**Code-based:**

- Verify router is registered in `main.py`
- Check for syntax errors
- Restart the server

**Configuration-based:**

- Check JSON syntax is valid
- Verify service is registered
- Ensure `enabled: true`
- Check logs for errors
- Restart the server

### Authentication Not Working

- Verify `api_keys` in `settings.json`
- Check `requires_auth` setting
- Ensure `X-API-Key` header is sent
- Check logs for auth errors

### Parameters Not Working

- Verify parameter mapping in configuration
- Check parameter source (query/path) matches request
- Ensure parameter keys match exactly
- Test with curl to isolate issues

## Next Steps

- [Creating Services](creating-services.md) - Build robust services
- [Authentication](authentication.md) - Secure your endpoints
- [Built-in Endpoints](builtin-endpoints.md) - Use what's included
- [Testing](../development/testing.md) - Write tests for endpoints
