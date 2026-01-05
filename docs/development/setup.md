# Development Setup

Set up Apiary for development work.

## Quick Setup

```bash
git clone https://github.com/lancereinsmith/apiary.git
cd apiary
uv sync
cp settings_template.json settings.json
cp config/endpoints_template.json config/endpoints.json
```

## Running in Development

```bash
# With auto-reload (recommended)
uv run apiary serve --reload

# Or using uvicorn directly
uvicorn app:api --reload --port 8000
```

## Apiary Project Structure

```text
apiary/
├── config/              # Configuration management
│   ├── settings.py      # Pydantic Settings
│   └── endpoint_config.py  # Endpoint loader
├── core/                # Core framework
│   ├── auth/            # Authentication & authorization
│   ├── services/        # Base service classes
│   ├── exceptions.py    # Custom exceptions
│   ├── middleware.py    # Middleware components
│   ├── rate_limiter.py  # Rate limiting logic
│   ├── metrics.py       # Metrics collection
│   ├── cache.py         # Caching utilities
│   └── router_factory.py # Dynamic router creation
├── routers/             # API route handlers
│   ├── auth.py          # Auth endpoints
│   ├── health.py        # Health checks
│   ├── metrics.py       # Metrics endpoint
│   └── endpoints.py     # Endpoint discovery
├── services/            # Business logic services
│   ├── crypto_service.py # Example service
│   └── __init__.py      # Service registration
├── models/              # Pydantic models
│   ├── requests.py      # Request models
│   └── responses.py     # Response models
├── templates/           # Jinja2 templates
├── static/              # Static assets
├── tests/               # Test suite
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── app.py               # FastAPI application factory
└── cli.py               # CLI commands
```

## Key Files

### `app.py`
FastAPI application factory. Creates and configures the FastAPI app instance. This is the main application module that can be imported by uvicorn, gunicorn, or other ASGI servers.

**Usage:**
- Import: `from app import api`
- Run with uvicorn: `uvicorn app:api`
- Run with gunicorn: `gunicorn app:api`
- Run with CLI: `uv run apiary serve`

### `config/settings.py`
Pydantic Settings class that loads configuration from `settings.json` and environment variables.

### `config/endpoint_config.py`
Loads and validates endpoint configuration from `config/endpoints.json`.

### `core/router_factory.py`
Creates dynamic FastAPI routers from endpoint configuration.

### `core/services/base.py`
Base service class that all services must inherit from.

## Development Tools

```bash
# Format code
black .

# Lint code
ruff check .
ruff check --fix .  # Auto-fix

# Type check
mypy .

# Run tests
pytest
pytest --cov  # With coverage
```

## Working with Services

### Creating a New Service

1. Create service file in `services/`
2. Inherit from `BaseService`
3. Implement `async def call(self, parameters)`
4. Register in `services/__init__.py`

Example:

```python
# services/weather_service.py
from core.services.base import BaseService

class WeatherService(BaseService):
    async def call(self, parameters=None):
        # Your logic here
        return {"temperature": 72}
```

```python
# services/__init__.py
from core.services import register_service
from services.weather_service import WeatherService

register_service("weather", WeatherService)
```

### Adding Configuration-Based Endpoints

Edit `config/endpoints.json`:

```json
{
  "path": "/api/weather",
  "method": "GET",
  "service": "weather",
  "enabled": true,
  "requires_auth": false
}
```

### Adding Code-Based Endpoints

Create a router in `routers/`:

```python
# routers/custom.py
from fastapi import APIRouter

router = APIRouter(prefix="/custom", tags=["custom"])

@router.get("/")
async def custom_endpoint():
    return {"message": "Custom endpoint"}
```

Register in `app.py` (in `_configure_routing` function):

```python
from routers import custom

def _configure_routing(api: fastapi.FastAPI, settings) -> None:
    # ... existing routers ...
    api.include_router(custom.router)
```

## Next Steps

- [Testing](testing.md) - Write tests for your changes
- [Code Quality](code-quality.md) - Maintain code quality
- [Project Structure](structure.md) - Deep dive into architecture
