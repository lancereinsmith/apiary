# Creating Services

Learn how to create reusable services for your Apiary API.

## What is a Service?

A service encapsulates business logic that can be called by endpoints. Services:

- ✅ Contain business logic
- ✅ Can be reused by multiple endpoints
- ✅ Are testable in isolation
- ✅ Support dependency injection
- ✅ Work with configurable endpoints

## Base Service Interface

All services should inherit from `BaseService`:

```python
from typing import Any, Dict, Optional
from core.services.base import BaseService

class MyService(BaseService):
    """My custom service."""

    async def call(
        self, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute the service.

        Args:
            parameters: Request parameters

        Returns:
            Service response dictionary
        """
        parameters = parameters or {}

        # Your business logic here
        result = await self._do_something(parameters)

        return {"result": result}
```

## Creating a Service

### Step 1: Create Service File

Create a new file in `services/`:

```python
"""Weather service."""

from typing import Any, Dict, Optional
import httpx
from core.services.base import BaseService
from core import ValidationError

class WeatherService(BaseService):
    """Service for fetching weather data."""

    async def call(
        self, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get weather for a city.

        Args:
            parameters: Must include 'city' key

        Returns:
            Weather data dictionary

        Raises:
            ValidationError: If city not provided or API fails
        """
        parameters = parameters or {}
        city = parameters.get("city")

        if not city:
            raise ValidationError("City parameter is required")

        # Fetch weather data
        weather_data = await self._fetch_weather(city)

        return {
            "city": city,
            "temperature": weather_data["temp"],
            "condition": weather_data["condition"],
        }

    async def _fetch_weather(self, city: str) -> Dict[str, Any]:
        """Fetch weather from external API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.weatherapi.com/v1/current.json",
                params={"q": city}
            )

            if response.status_code != 200:
                raise ValidationError(f"Failed to fetch weather for {city}")

            data = response.json()
            return {
                "temp": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
            }
```

### Step 2: Register Service

Add to `services/__init__.py`:

```python
from core.services import register_service
from services.weather_service import WeatherService

register_service("weather", WeatherService)
```

### Step 3: Use in Endpoint

Configuration-based:

```json
{
  "path": "/api/weather",
  "method": "GET",
  "service": "weather",
  "enabled": true,
  "parameters": {
    "city": {
      "source": "query",
      "key": "city"
    }
  }
}
```

Code-based:

```python
@router.get("/weather")
async def get_weather(city: str):
    service = WeatherService()
    result = await service.call({"city": city})
    return result
```

## Service Patterns

### Simple Data Service

```python
class DataService(BaseService):
    """Simple data retrieval service."""

    async def call(self, parameters=None):
        return {
            "data": "Hello, World!",
            "timestamp": self._get_timestamp()
        }
```

### External API Service

```python
class APIService(BaseService):
    """Service that calls external API."""

    async def call(self, parameters=None):
        parameters = parameters or {}
        endpoint = parameters.get("endpoint", "default")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.example.com/{endpoint}"
            )
            return response.json()
```

### Database Service

```python
class DatabaseService(BaseService):
    """Service that queries database."""

    async def call(self, parameters=None):
        parameters = parameters or {}
        user_id = parameters.get("user_id")

        # Query database
        user = await self._get_user(user_id)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
```

### Aggregation Service

```python
class AggregationService(BaseService):
    """Service that combines multiple data sources."""

    async def call(self, parameters=None):
        # Call multiple services
        weather = await WeatherService().call({"city": "London"})
        news = await NewsService().call({"category": "tech"})

        return {
            "weather": weather,
            "news": news,
        }
```

## Best Practices

### 1. Error Handling

Always handle errors appropriately:

```python
from core import ValidationError, NotFoundError

async def call(self, parameters=None):
    try:
        result = await self._fetch_data()
    except httpx.HTTPError as e:
        raise ValidationError(f"API error: {str(e)}")
    except KeyError as e:
        raise NotFoundError(f"Data not found: {str(e)}")

    return result
```

### 2. Input Validation

Validate all inputs:

```python
async def call(self, parameters=None):
    parameters = parameters or {}

    # Validate required parameters
    if "user_id" not in parameters:
        raise ValidationError("user_id is required")

    # Validate parameter types
    user_id = parameters["user_id"]
    if not isinstance(user_id, int):
        raise ValidationError("user_id must be an integer")

    # Continue with logic
    return await self._process(user_id)
```

### 3. Dependency Injection

Use constructor injection for dependencies:

```python
class MyService(BaseService):
    """Service with dependencies."""

    def __init__(self, http_client: httpx.AsyncClient = None):
        super().__init__()
        self.http_client = http_client or httpx.AsyncClient()

    async def call(self, parameters=None):
        response = await self.http_client.get("https://api.example.com")
        return response.json()
```

### 4. Logging

Add logging for debugging:

```python
import logging

logger = logging.getLogger(__name__)

class MyService(BaseService):
    async def call(self, parameters=None):
        logger.info("Service called", extra={"parameters": parameters})

        try:
            result = await self._process(parameters)
            logger.info("Service completed successfully")
            return result
        except Exception as e:
            logger.error(f"Service failed: {str(e)}")
            raise
```

### 5. Testing

Write unit tests for services:

```python
import pytest
from services.weather_service import WeatherService

@pytest.mark.asyncio
async def test_weather_service():
    service = WeatherService()
    result = await service.call({"city": "London"})

    assert "city" in result
    assert result["city"] == "London"
    assert "temperature" in result
```

## Next Steps

- [Adding Endpoints](adding-endpoints.md) - Use your services in endpoints
- [Authentication](authentication.md) - Secure your services
- [Testing](../development/testing.md) - Write tests for services

