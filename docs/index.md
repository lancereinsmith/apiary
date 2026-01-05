# 🐝 Apiary

## A Modular, Extensible FastAPI Framework

**Apiary** is a production-ready FastAPI framework designed for building modular, extensible REST APIs with minimal code. It provides a robust foundation with authentication, rate limiting, metrics, health checks, and a unique configuration-driven endpoint system.

## Key Features

### Production-Ready

- **Structured logging** with correlation IDs
- **Rate limiting** with configurable limits
- **Health checks** (liveness and readiness probes)
- **Metrics collection** for monitoring
- **Request validation** and size limits
- **Caching support** with cache headers

### Security

- **API key authentication** with flexible authorization
- **Security headers** middleware
- **CORS support** for cross-origin requests
- **Input sanitization** and validation

### Modular & Extensible

- **Configuration-driven endpoints** - add endpoints without code changes
- **Service-based architecture** with dependency injection
- **Plugin system** for custom services
- **Endpoint discovery** API

### Developer Experience

- **Type-safe configuration** using Pydantic Settings
- **Comprehensive error handling** with standardized responses
- **Auto-generated API documentation** (Swagger UI & ReDoc)
- **Testing utilities** with mocks and fixtures
- **Code quality tools** (black, ruff, mypy)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/lancereinsmith/apiary.git
cd apiary

# Install dependencies
uv sync

# Create configuration
cp settings_template.json settings.json
cp config/endpoints_template.json config/endpoints.json

# Run the application
uv run apiary serve --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

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

### Built-in Production Features

- **Rate Limiting**: Per-endpoint limits with different rates for authenticated users
- **Metrics**: Track request counts, response times, and error rates
- **Health Checks**: Kubernetes-compatible liveness and readiness probes
- **Caching**: Response caching with configurable TTLs
- **Logging**: Structured logging with correlation IDs

## Use Cases

Apiary is perfect for:

- **Personal APIs**: Quickly build APIs for personal projects
- **Microservices**: Create modular, maintainable microservices
- **API Gateways**: Build custom API gateways with routing and aggregation
- **Rapid Prototyping**: Test ideas with configuration-driven endpoints
- **Learning**: Study production-ready FastAPI architecture

## Architecture Overview

```text
apiary/
├── config/              # Configuration management
│   ├── settings.py      # Pydantic Settings
│   └── endpoint_config.py  # Endpoint loader
├── core/                # Core utilities
│   ├── auth/            # Authentication & authorization
│   ├── services/        # Base service classes
│   ├── exceptions.py    # Custom exceptions
│   ├── middleware.py    # Custom middleware
│   ├── rate_limiter.py  # Rate limiting
│   ├── metrics.py       # Metrics collection
│   └── cache.py         # Caching utilities
├── routers/             # API route handlers
├── services/            # Business logic services
├── models/              # Request/response models
├── templates/           # HTML templates
├── app.py               # FastAPI application factory
└── cli.py               # CLI commands
```

## Built-in Endpoints

- `GET /` - Landing page
- `GET /health` - Health check
- `GET /health/live` - Liveness probe
- `GET /health/ready` - Readiness probe
- `GET /metrics` - Application metrics
- `GET /endpoints` - Endpoint discovery
- `GET /auth/status` - Authentication status
- `GET /auth/validate` - Validate API key

## Next Steps

1. [Installation Guide](getting-started/installation.md) - Set up your environment
2. [Quick Start](getting-started/quickstart.md) - Build your first API
3. [Configuration](getting-started/configuration.md) - Configure your application
4. [Adding Endpoints](guide/adding-endpoints.md) - Learn to add endpoints
5. [Creating Services](guide/creating-services.md) - Build custom services

## Community & Support

- **Documentation**: [Read the full docs](getting-started/installation.md)
- **Contributing**: [Contribution Guidelines](about/contributing.md)
- **Issues**: [GitHub Issues](https://github.com/lancereinsmith/apiary/issues)
- **Discussions**: [GitHub Discussions](https://github.com/lancereinsmith/apiary/discussions)

## License

This project is open source and available under the [MIT License](about/license.md).

