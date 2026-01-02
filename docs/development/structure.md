# Project Structure

Understand the Apiary codebase structure.

## Directory Layout

```text
apiary/
├── config/              # Configuration management
│   ├── __init__.py
│   ├── settings.py      # Pydantic Settings
│   └── endpoint_config.py  # Endpoint loader
├── core/                # Core utilities
│   ├── __init__.py
│   ├── auth/            # Authentication & authorization
│   │   ├── __init__.py
│   │   ├── authentication.py
│   │   └── authorization.py
│   ├── services/        # Base service classes
│   │   ├── __init__.py
│   │   └── base.py
│   ├── cache.py         # Caching utilities
│   ├── dependencies.py  # Dependency injection
│   ├── exceptions.py    # Custom exceptions
│   ├── logging_config.py  # Logging setup
│   ├── metrics.py       # Metrics collection
│   ├── middleware.py    # Custom middleware
│   ├── rate_limiter.py  # Rate limiting
│   └── request_validation.py  # Request validation
├── models/              # Data models
│   ├── requests.py      # Request models
│   └── responses.py     # Response models
├── routers/             # API route handlers
│   ├── __init__.py
│   ├── auth.py          # Authentication endpoints
│   ├── endpoints.py     # Endpoint discovery
│   ├── health.py        # Health checks
│   ├── home.py          # Landing page
│   └── metrics.py       # Metrics endpoint
├── services/            # Business logic services
│   ├── __init__.py
│   ├── crypto.py        # Crypto service (legacy)
│   └── crypto_service.py  # Crypto service (new)
├── static/              # Static files
│   ├── css/
│   └── img/
├── templates/           # HTML templates
│   ├── home/
│   └── shared/
├── tests/               # Test suite
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── main.py              # Application entry point
├── settings.json        # Configuration (not in repo)
├── pyproject.toml       # Project dependencies
└── README.md            # Project README
```

## Key Files

### `main.py`

Application entry point. Configures FastAPI app, middleware, and routers.

### `config/settings.py`

Pydantic Settings for type-safe configuration.

### `core/exceptions.py`

Custom exception classes for error handling.

### `core/middleware.py`

Custom middleware for logging, request IDs, etc.

### `core/auth/`

Authentication and authorization logic.

### `services/`

Business logic services that can be called by endpoints.

### `routers/`

FastAPI routers for handling HTTP requests.

## Adding New Components

### New Service

1. Create file in `services/`
2. Inherit from `BaseService`
3. Register in `services/__init__.py`

### New Router

1. Create file in `routers/`
2. Create `APIRouter` instance
3. Register in `main.py`

### New Model

1. Add to `models/requests.py` or `models/responses.py`
2. Use in router endpoints

## Next Steps

- [Development Setup](setup.md) - Set up environment
- [Testing](testing.md) - Write tests
- [Adding Endpoints](../guide/adding-endpoints.md) - Create endpoints

