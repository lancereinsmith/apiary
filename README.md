# 🐝 Apiary

**A modular, extensible FastAPI framework for building production-ready REST APIs with minimal code.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![bees](static/img/bees.gif)

## Overview

Apiary is a production-ready FastAPI framework that combines the power of FastAPI with a unique configuration-driven endpoint system. Build APIs quickly with built-in authentication, rate limiting, metrics, health checks, and more.

## Key Features

### Production-Ready

- **Structured logging** with correlation IDs for request tracking
- **Rate limiting** with configurable limits per endpoint
- **Health checks** - Kubernetes-compatible liveness and readiness probes
- **Metrics collection** for monitoring and observability
- **Request validation** and size limits
- **Caching support** with configurable TTLs

### Security

- **API key authentication** with flexible authorization
- **Security headers** middleware
- **CORS support** for cross-origin requests
- **Input sanitization** and validation

### Modular & Extensible

- **Configuration-driven endpoints** - add endpoints without code changes
- **Service-based architecture** with dependency injection
- **Plugin system** for custom services

## Quick Start

```bash
# Clone the repository
git clone https://github.com/lancereinsmith/apiary.git
cd apiary

# Install dependencies (requires uv)
uv sync

# Create configuration
cp settings_template.json settings.json
cp config/endpoints_template.json config/endpoints.json

# Run the application
python main.py
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## CLI

Apiary includes a CLI for common tasks:

```bash
uv run apiary serve --reload    # Dev server with auto-reload
uv run apiary test              # Run tests
uv run apiary check-all         # Code quality checks
uv run apiary docs-serve        # Serve docs locally
```

**[Full CLI reference →](https://lancereinsmith.github.io/apiary/development/cli/)**

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
└── main.py              # Application entry point
```

## Built-in Endpoints

- `GET /` - Landing page (can disable in `settings.json`)
- `GET /health` - Health check
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe
- `GET /metrics` - Application metrics
- `GET /endpoints` - Endpoint discovery
- `GET /auth/status` - Authentication status
- `GET /auth/validate` - Validate API key

## Use Cases

Apiary is perfect for:

- **Personal APIs** - Quickly build APIs for personal projects
- **Microservices** - Create modular, maintainable microservices
- **API Gateways** - Build custom API gateways with routing and aggregation

## Development

```bash
# Install dependencies
uv sync

# Run development server
uv run apiary serve --reload

# Run tests
uv run apiary test

# Format and lint
uv run apiary check-all
```

See the [Development Guide](https://lancereinsmith.github.io/apiary/development/setup/) for details.

## Deployment

### Quick Deployment

```bash
# On your server
git clone https://github.com/lancereinsmith/apiary.git <target folder>
cd apiary
uv sync

# Configure
cp settings_template.json settings.json
# Edit settings.json with production values

# Set up nginx (see _server/nginx/)
# Set up systemd (see _server/units/)
# Enable SSL with Let's Encrypt

sudo systemctl enable apiary
sudo systemctl start apiary
```

See the [Deployment Guide](https://lancereinsmith.github.io/apiary/deployment/overview/) for detailed instructions.

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
register_service("weather", WeatherService)
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

## Testing

```bash
uv run apiary test        # Run tests
uv run apiary coverage    # With coverage
```

See the [Testing Guide](https://lancereinsmith.github.io/apiary/development/testing/) for details.

## Configuration

### Application Settings (`settings.json`)

```json
{
  "api_keys": "your-api-key-1,your-api-key-2",
  "enable_landing_page": true,
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,
  "rate_limit_per_minute_authenticated": 300
}
```

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

See the [Contributing Guide](https://lancereinsmith.github.io/apiary/about/contributing/) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Inspired by modern API best practices
- Documentation powered by [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)

## Support

- **Documentation**: [Read the docs](https://lancereinsmith.github.io/apiary/)
- **Issues**: [GitHub Issues](https://github.com/lancereinsmith/apiary/issues)
- **Discussions**: [GitHub Discussions](https://github.com/lancereinsmith/apiary/discussions)

## Stars

If you find Apiary useful, please consider giving it a star on GitHub!

---
