# Quick Start

Get up and running with Apiary in minutes! This guide will walk you through creating your first API endpoint.

## Prerequisites

Make sure you've completed the [Installation](installation.md) guide.

## Start the Server

First, start the development server:

```bash
# Option 1: Using CLI (recommended)
uv run apiary serve --reload

# Option 2: Using uvicorn directly
uvicorn app:api --reload
```

You should see:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Visit `http://localhost:8000` - you should see the landing page.

## Explore Built-in Endpoints

Apiary comes with several built-in endpoints:

### Health Check

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### Endpoint Discovery

```bash
curl http://localhost:8000/endpoints
```

This shows all available and enabled configurable endpoints and services.

### API Documentation

Visit these URLs in your browser:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Create Your First Endpoint (Configuration-Based)

The easiest way to add an endpoint is through configuration.

### Step 1: Understand the Example

Apiary includes a sample crypto service. Let's look at the configuration in `config/endpoints.json`:

```json
{
  "endpoints": [
    {
      "path": "/api/crypto",
      "method": "GET",
      "service": "crypto",
      "enabled": true,
      "requires_auth": false,
      "description": "Get cryptocurrency price data. Accepts optional 'symbol' parameter (e.g., BTC, ETH, SOL). Defaults to BTC if not provided.",
      "tags": ["crypto"],
      "summary": "Cryptocurrency price data"
    }
  ]
}
```

### Step 2: Test the Example Endpoint

```bash
# Get Bitcoin price (default)
curl http://localhost:8000/api/crypto

# Get Ethereum price
curl http://localhost:8000/api/crypto?symbol=ETH

# Get Solana price
curl http://localhost:8000/api/crypto?symbol=SOL
```

### Step 3: Enable the Hello Endpoint

Apiary includes a sample hello service, but it's not enabled by default. Let's add it to your configuration.

Edit `config/endpoints.json` and add the hello endpoint to the endpoints array:

```json
{
  "endpoints": [
    {
      "path": "/api/crypto",
      "method": "GET",
      "service": "crypto",
      "enabled": true,
      "requires_auth": false,
      "description": "Get cryptocurrency price data. Accepts optional 'symbol' parameter (e.g., BTC, ETH, SOL). Defaults to BTC if not provided.",
      "tags": ["crypto"],
      "summary": "Cryptocurrency price data"
    },
    {
      "path": "/api/hello",
      "method": "GET",
      "service": "hello",
      "enabled": true,
      "requires_auth": false,
      "description": "Hello world endpoint. Accepts optional 'name' parameter (e.g., ?name=Alice). Defaults to World if not provided.",
      "tags": ["demo"],
      "summary": "Hello world greeting"
    }
  ]
}
```

!!! note
    Each endpoint specifies a `service` that handles the business logic. The `crypto` service fetches cryptocurrency data, while the `hello` service returns a greeting message.

### Step 4: Test the Hello Endpoint

Restart the server to load the new configuration, then test the hello endpoint:

```bash
# Default hello
curl http://localhost:8000/api/hello

# Hello with name parameter
curl http://localhost:8000/api/hello?name=Alice
```

Response:

```json
{
  "message": "Hello, Alice!",
  "name": "Alice",
  "service": "hello"
}
```

## Understanding the Hello Service

Let's look at how the hello service is implemented. The service is already created in `services/hello_service.py`:

```python
"""Hello world service for demonstration purposes."""

from typing import Any, Dict, Optional
from core.services.base import BaseService

class HelloService(BaseService):
    """Service that returns a simple hello world message.

    This service demonstrates the simplest possible BaseService implementation.
    It doesn't require external API calls and returns a static response
    with optional customization via parameters.
    """

    service_name = "hello"

    async def call(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return a hello world message.

        Args:
            parameters: Optional service parameters dictionary containing:
                - name (str, optional): Name to greet. Defaults to "World".

        Returns:
            Dictionary containing a greeting message.
        """
        # Extract name from parameters, defaulting to "World"
        name = "World"
        if parameters and "name" in parameters:
            provided_name = str(parameters["name"]).strip()
            if provided_name:
                name = provided_name

        # Return greeting response
        return {
            "message": f"Hello, {name}!",
            "name": name,
            "service": self.service_name,
        }
```

Key points about services:

1. **Inherit from `BaseService`**: All services must extend the base class
2. **Implement `call()` method**: This async method handles the business logic
3. **Accept parameters**: The `parameters` dict contains query params, path params, or configured values
4. **Return a dict**: Services return JSON-serializable dictionaries

### Service Registration

Services are **automatically discovered and registered** from the `services/`
directory. Service files should have a `_service.py` suffix. Each service class
can optionally define a `service_name` attribute to control how it's registered:

```python
class HelloService(BaseService):
    """Service that returns a simple hello world message."""

    service_name = "hello"  # Registers as "hello"

    async def call(self, parameters: Optional[Dict[str, Any]] = None):
        # ... implementation
```

If `service_name` is not specified, the service name defaults to the filename
without the `_service.py` suffix.

The name you use (e.g., `"hello"`) is what you reference in `config/endpoints.json`.

## Create Your Own Custom Service

Now let's walk through creating a brand new service from scratch.

### Step 1: Create Service File

Create a new file `services/weather_service.py`:

```python
"""Weather service example."""

from typing import Any, Dict, Optional
from core.services.base import BaseService

class WeatherService(BaseService):
    """Service that returns mock weather data."""

    service_name = "weather"  # Optional: explicitly set registration name

    async def call(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return weather information.

        Args:
            parameters: Optional parameters with 'city' field

        Returns:
            Weather data dictionary
        """
        city = "Unknown"
        if parameters and "city" in parameters:
            city = str(parameters["city"]).strip() or "Unknown"

        # In a real service, you'd call an external API here
        return {
            "city": city,
            "temperature": 72,
            "condition": "Sunny",
            "service": self.service_name  # Can only return like this if explicitly set
        }
```

### Step 2: Configure the Endpoint

Add to `config/endpoints.json`:

```json
{
  "path": "/api/weather",
  "method": "GET",
  "service": "weather",
  "enabled": true,
  "requires_auth": false,
  "description": "Get weather information. Accepts optional 'city' parameter.",
  "tags": ["weather"],
  "summary": "Weather information"
}
```

### Step 3: Test Your Service

Restart the server and test:

```bash
# Default weather
curl http://localhost:8000/api/weather

# Weather for specific city
curl http://localhost:8000/api/weather?city=Boston
```

Response:

```json
{
  "city": "Boston",
  "temperature": 72,
  "condition": "Sunny",
  "service": "weather"
}
```

## Add Authentication

Let's protect an endpoint with API key authentication.

### Step 1: Configure API Keys

Edit `config/settings.json`:

```json
{
  "api_keys": "secret-key-123,another-key-456",
  "enable_landing_page": true,
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,
  "rate_limit_per_minute_authenticated": 300
}
```

### Step 2: Create Protected Endpoint

Add to `config/endpoints.json`:

```json
{
  "path": "/api/hello/private",
  "method": "GET",
  "service": "hello",
  "enabled": true,
  "requires_auth": true,
  "description": "Protected hello endpoint (requires authentication)",
  "tags": ["demo"]
}
```

### Step 3: Test Authentication

```bash
# Without API key (should fail)
curl http://localhost:8000/api/hello/private

# With valid API key (should succeed)
curl -H "X-API-Key: secret-key-123" http://localhost:8000/api/hello/private
```

## Next Steps

Now that you have a working API, explore more features:

### Learn More

- [Configuration Guide](configuration.md) - Understand all configuration options
- [Adding Endpoints](../guide/adding-endpoints.md) - Learn both code-based and config-based approaches
- [Creating Services](../guide/creating-services.md) - Build more complex services
- [Authentication Guide](../guide/authentication.md) - Implement advanced auth patterns

### Deploy Your API

When you're ready for production:

1. [Server Setup](../deployment/server-setup.md) - Deploy to a server
2. [Configuration](../deployment/configuration.md) - Production configuration
3. [Monitoring](../deployment/monitoring.md) - Set up monitoring

## Common Tasks

### View Logs

Check the console output for structured logs:

```text
INFO 2024-01-01 12:00:00 [abc123] GET /api/hello - 200 OK (45ms)
```

### Check Metrics

```bash
curl http://localhost:8000/metrics
```

### List All Endpoints

```bash
curl http://localhost:8000/endpoints
```

### Enable/Disable Endpoint

Edit `config/endpoints.json` and set `enabled: false`:

```json
{
  "path": "/api/hello",
  "enabled": false
}
```

## Troubleshooting

### Server Won't Start

```bash
# Check if port is in use
lsof -i:8000

# Use different port
uvicorn app:api --port 8001
# Or: uv run apiary serve --port 8001
```

### Endpoint Not Found

1. Check `config/endpoints.json` is valid JSON
2. Verify service is registered in `services/__init__.py`
3. Restart the server
4. Check logs for errors

### Service Errors

1. Check service implementation
2. Verify `BaseService` is inherited
3. Ensure `call()` method is async
4. Check logs for detailed error messages

Continue to the [User Guide](../guide/overview.md) to learn more about Apiary's features.
