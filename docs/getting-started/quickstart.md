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

This shows all available configurable endpoints and services.

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
      "description": "Get cryptocurrency price data",
      "tags": ["crypto"]
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

### Step 3: Add Your Own Endpoint

Edit `config/endpoints.json` to add a new endpoint:

```json
{
  "endpoints": [
    {
      "path": "/api/crypto",
      "method": "GET",
      "service": "crypto",
      "enabled": true,
      "requires_auth": false,
      "description": "Get cryptocurrency price data",
      "tags": ["crypto"]
    },
    {
      "path": "/api/hello",
      "method": "GET",
      "service": "crypto",
      "enabled": true,
      "requires_auth": false,
      "description": "Hello world endpoint",
      "tags": ["demo"]
    }
  ]
}
```

!!! note
    You'll need to restart the server for configuration changes to take effect.

### Step 4: Restart and Test

```bash
# Restart the server (Ctrl+C then restart)
uv run apiary serve --reload
```

# Test your new endpoint
curl http://localhost:8000/api/hello
```

## Create a Custom Service

Now let's create a custom service for your endpoint.

### Step 1: Create Service File

Create `services/hello_service.py`:

```python
"""Hello world service."""

from typing import Any, Dict, Optional
from core.services.base import BaseService


class HelloService(BaseService):
    """Simple hello world service."""

    async def call(self, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return a hello message.

        Args:
            parameters: Request parameters (name optional)

        Returns:
            Dict with hello message
        """
        parameters = parameters or {}
        name = parameters.get("name", "World")

        return {
            "message": f"Hello, {name}!",
            "timestamp": self.get_timestamp()
        }

    def get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

### Step 2: Register the Service

Edit `services/__init__.py` to register your service:

```python
"""Services package initialization."""

from core.services import register_service

# Import and register services
from services.crypto_service import CryptoService
from services.hello_service import HelloService

# Register services by name
register_service("crypto", CryptoService)
register_service("hello", HelloService)

__all__ = ["CryptoService", "HelloService"]
```

### Step 3: Update Endpoint Configuration

Update `config/endpoints.json`:

```json
{
  "endpoints": [
    {
      "path": "/api/hello",
      "method": "GET",
      "service": "hello",
      "enabled": true,
      "requires_auth": false,
      "description": "Hello world endpoint. Accepts optional 'name' parameter.",
      "tags": ["demo"],
      "parameters": {
        "name": {
          "source": "query",
          "key": "name"
        }
      }
    }
  ]
}
```

### Step 4: Test Your Service

Restart the server and test:

```bash
# Default hello
curl http://localhost:8000/api/hello

# Hello with name
curl http://localhost:8000/api/hello?name=Alice
```

Response:

```json
{
  "message": "Hello, Alice!",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

## Add Authentication

Let's protect an endpoint with API key authentication.

### Step 1: Configure API Keys

Edit `settings.json`:

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

### Try These Features

1. **Rate Limiting**: Configure different limits for public/authenticated users
2. **Metrics**: Check `/metrics` to see request statistics
3. **Caching**: Add cache headers to reduce load
4. **Health Checks**: Integrate with monitoring systems

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
curl http://localhost:8000/endpoints | jq
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
# Or: uv run apiary serve 127.0.0.1 8001
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

## Example Projects

Check the `examples/` directory for more examples:

- Simple CRUD API
- Weather service integration
- Multi-service aggregation
- Authentication patterns

## Getting Help

- 📖 Read the [full documentation](../guide/overview.md)
- 💬 Join [GitHub Discussions](https://github.com/lancereinsmith/apiary/discussions)
- 🐛 Report issues on [GitHub](https://github.com/lancereinsmith/apiary/issues)

## What's Next?

You now have a working API! Here are some ideas:

1. **Add more services**: Create services for weather, news, database queries
2. **Implement caching**: Reduce external API calls
3. **Add monitoring**: Track performance and errors
4. **Deploy to production**: Use nginx + systemd or Docker
5. **Build a frontend**: Create a UI for your API

Continue to the [User Guide](../guide/overview.md) to learn more about Apiary's features.

