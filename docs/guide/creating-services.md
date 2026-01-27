# Creating Services

Learn how to create reusable services for your Apiary API.

## What is a Service?

A service encapsulates business logic that can be called by endpoints.

Services:

- Contain business logic
- Can be reused by multiple endpoints (configurable)
- Support dependency injection

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

Create a new `{service_name}_service.py` file. Use **`services_custom/`** for custom
services (recommended for deployment) or `services/` for in-repo development.

!!! important "Use services_custom/ for Deployments"
    Put custom services in **`services_custom/`**, not `services/`. The `services_custom/`
    directory is gitignored, so your code is never overwritten when you `git pull` updates.
    Run `uv run apiary init` to create it. The `services/` directory is for built-in
    services and is updated by upstream.

```python
# services_custom/weather_service.py (or services/ for in-repo only)
"""Weather service."""

from typing import Any, Dict, Optional
import httpx
from core.services.base import BaseService
from core import ValidationError

class WeatherService(BaseService):
    """Service for fetching weather data."""

    # Optional: Define custom service name for registration
    # If not specified, uses filename without '_service.py'
    service_name = "weather"

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

### Step 2: Service Registration

Services are **automatically discovered** from `services/` and `services_custom/`.
No explicit registration needed - create your service file and it's available.
Custom services in `services_custom/` are loaded after built-ins, so a custom
service with the same name overrides a built-in.

**Service Name**: The registration name comes from the `service_name` class
attribute. If not defined, it falls back to the filename without the
`_service.py` suffix, if present.

```python
# services_custom/weather_service.py

class WeatherService(BaseService):
    service_name = "weather"  # Registers as "weather"
    # ... rest of implementation
```

```python
# services_custom/stock.py (without service_name attribute)

class StockService(BaseService):
    # Automatically registers as "stock" (from filename)
    # ... rest of implementation
```

!!! info "How Auto-Discovery Works"
    The application scans `services/` (built-in) and `services_custom/` (your code) for
    Python files and registers any class that inherits from `BaseService`. Custom
    services are loaded after built-ins. Both directories are scanned on application
    startup.

#### Service Naming Examples

```python

## Explicit name (recommended for clarity)

class WeatherService(BaseService):
    service_name = "weather"  # Registers as "weather"
```

```python

## Filename fallback: services_custom/stock_data_service.py

class StockDataService(BaseService):
    # No service_name defined

    # Automatically registers as "stock_data" (from filename without '_service.py')
```

```python

## Short filename: services_custom/email.py

class EmailService(BaseService):
    # No service_name defined

    # Automatically registers as "email" (from filename)
```

#### Multiple Services in One File

You can define **multiple services in a single file**. Each service class that inherits from `BaseService` will be auto-discovered and registered independently:

```python
# services_custom/weather_services.py

from typing import Any, Dict, Optional
from core.services.base import BaseService

class CurrentWeatherService(BaseService):
    """Service for current weather data."""

    service_name = "current_weather"  # Must be unique!

    async def call(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Implementation here
        return {"temperature": 72, "condition": "sunny"}

class WeatherForecastService(BaseService):
    """Service for weather forecast data."""

    service_name = "forecast"  # Different name required!

    async def call(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Implementation here
        return {"forecast": [{"day": "Monday", "temp": 75}]}

class WeatherAlertsService(BaseService):
    """Service for weather alerts."""

    service_name = "weather_alerts"

    async def call(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Implementation here
        return {"alerts": []}
```

!!! warning "Unique Service Names Required"
    Each service class **must** define a unique `service_name` attribute. If you omit it, all services in the file will default to the same name (the filename without `_service.py`), causing later services to overwrite earlier ones.

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
from services_custom.weather_service import WeatherService
...
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

### 1. Input Validation

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

### 2. Dependency Injection

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

## Next Steps

- [Adding Endpoints](adding-endpoints.md) - Use your services in endpoints
- [Authentication](authentication.md) - Secure your services
