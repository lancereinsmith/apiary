# 🐝 Apiary

**A modular, extensible FastAPI framework for building production-ready REST APIs with minimal code.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![bees](static/img/bees.gif)

## Overview

Apiary is a FastAPI framework that combines the power of FastAPI with a unique configuration-driven endpoint system. Build APIs quickly with built-in authentication, rate limiting, metrics, health checks, and more.

## Key Features

### Modular & Extensible

- **Configuration-driven endpoints** - add endpoints without code changes
- **Service-based architecture** with dependency injection
- **Plugin system** for custom services

### Security

- **API key authentication** with flexible authorization
- **Security headers** middleware
- **CORS support** for cross-origin requests
- **Input sanitization** and validation

## Quick Start

```bash
# Clone the repository
git clone https://github.com/lancereinsmith/apiary.git
cd apiary

# Install dependencies (requires uv)
uv sync

# Create configuration
uv run apiary init

# Run the application
uv run apiary serve --reload
# Or using uvicorn directly
uvicorn app:api --reload
```

Go to `http://localhost:8000/docs` for interactive API documentation. (Can be disabled.)

## CLI

Apiary includes a CLI for common tasks:

```bash
uv run apiary init              # Initialize config files
uv run apiary serve --reload    # Dev server with auto-reload
uv run apiary validate-config   # Validate API key config
uv run apiary clean             # Clean up generated files
```

**[Full CLI reference →](https://lancereinsmith.github.io/apiary/reference/cli/)**

## Documentation

**[Read the full documentation →](https://lancereinsmith.github.io/apiary/)**

- [Installation](https://lancereinsmith.github.io/apiary/getting-started/installation/) - Get started
- [Quick Start](https://lancereinsmith.github.io/apiary/getting-started/quickstart/) - Build your first API
- [User Guide](https://lancereinsmith.github.io/apiary/guide/overview/) - Learn all features
- [API Reference](https://lancereinsmith.github.io/apiary/reference/core/) - Technical docs

## What Makes Apiary Different?

### Configuration-Driven Endpoints

Add new API endpoints without writing code - just edit a JSON configuration file:

```json
{
  "endpoints": [
    {
      "path": "/api/crypto",
      "method": "GET",
      "service": "crypto",
      "enabled": true,
      "requires_auth": false,
      "description": "Get cryptocurrency price data"
    }
  ]
}
```

### Service-Based Architecture

Create reusable services that can be called by multiple endpoints:

```python
from core.services.base import BaseService

class MyService(BaseService):
    async def call(self, parameters=None):
        # Your business logic here
        return {"result": "data"}
```

Register the service and use it in configurable endpoints or code-based routes.

## Architecture

```text
apiary/
├── config/              # Configuration management
├── core/                # Core utilities (auth, middleware, etc.)
├── routers/             # API route handlers
├── services/            # Business logic services
├── models/              # Request/response models
├── templates/           # HTML templates
├── static/              # Static files
├── app.py               # FastAPI application factory
└── cli.py               # CLI commands
```

## Built-in Endpoints (can be disabled)

- `GET /` - Landing page (can disable in `config/settings.json`)
- `GET /health` - Health check
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe
- `GET /metrics` - Application metrics
- `GET /endpoints` - Endpoint discovery
- `GET /auth/status` - Authentication status
- `POST /auth/validate` - Validate API key

## Use Cases

Apiary is perfect for:

- **Personal APIs** - Quickly build APIs for personal projects
- **Microservices** - Create modular, maintainable microservices
- **API Gateways** - Build custom API gateways with routing and aggregation

## Example: Adding a Service

1. **Create service** in `services/weather_service.py`:

    ```python
    from core.services.base import BaseService

    class WeatherService(BaseService):
        async def call(self, parameters=None):
            city = parameters.get("city", "London")
            # Fetch weather data...
            return {"city": city, "temp": 20}
    ```

1. **Register service** in `services/__init__.py`:

    ```python
    from services.weather_service import WeatherService

    # Services are auto-discovered and registered by class name
    ```

1. **Add endpoint** in `config/endpoints.json`:

    ```json
    {
      "path": "/api/weather",
      "method": "GET",
      "service": "weather",
      "enabled": true,
      "requires_auth": false
    }
    ```

That's it! Restart the server and your endpoint is live.

## Configuration

### Application Settings (`config/settings.json`)

```json
{
  "api_keys": "your-api-key-1,your-api-key-2",
  "enable_landing_page": true,
  "enable_docs": true,
  "enable_redoc": true,
  "enable_openapi": true,
  "enabled_routers": ["health", "metrics", "auth", "endpoints"],
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,
  "rate_limit_per_minute_authenticated": 300
}
```

**Tip**: API keys can also be file paths (e.g., `"config/api_keys.txt"`) for easier management.

### Endpoint Configuration (`config/endpoints.json`)

```json
{
  "endpoints": [
    {
      "path": "/api/example",
      "method": "GET",
      "service": "example",
      "enabled": true,
      "requires_auth": false,
      "description": "Example endpoint"
    }
  ]
}
```

## Deployment

### Quick Deployment

```bash
# On your server
git clone https://github.com/lancereinsmith/apiary.git
cd apiary
uv sync

# Initialize configuration
uv run apiary init
# Edit config/settings.json with production values

# Set up nginx (see _server/nginx/)
# Set up systemd (see _server/systemd/)
# Enable SSL with Let's Encrypt

sudo systemctl enable apiary
sudo systemctl start apiary
```

### Updating Your Deployment

Apiary is designed for **update-safe deployments**. Config and custom code are gitignored:

```bash
cd /path/to/apiary
git pull origin main  # Your config and custom code won't be touched!
uv sync               # Update dependencies
sudo systemctl restart apiary
```

- **Config**: `config/settings.json`, `config/endpoints.json`, API key files
- **Custom code**: put services in `services_custom/` and routers in `routers_custom/` (created by `uv run apiary init`) so they are never overwritten by `git pull`

See the [Deployment Guide](https://lancereinsmith.github.io/apiary/deployment/overview/) for detailed instructions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

See the [Contributing Guide](https://lancereinsmith.github.io/apiary/about/contributing/) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Documentation powered by [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)

## Support

- **Documentation**: [Read the docs](https://lancereinsmith.github.io/apiary/)
- **Issues**: [GitHub Issues](https://github.com/lancereinsmith/apiary/issues)

## Stars

If you find Apiary useful, please consider giving it a star on GitHub!

---
