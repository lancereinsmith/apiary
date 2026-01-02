# User Guide Overview

Welcome to the Apiary User Guide! This guide covers everything you need to know to build production-ready APIs with Apiary.

## What You'll Learn

This guide is organized into the following sections:

### Core Concepts

1. **[Adding Endpoints](adding-endpoints.md)** - Learn how to create API endpoints
   - Code-based endpoints (traditional FastAPI)
   - Configuration-based endpoints (Apiary's unique feature)
   - When to use each approach

2. **[Creating Services](creating-services.md)** - Build reusable business logic
   - Service architecture
   - Base service interface
   - Best practices for services

3. **[Authentication](authentication.md)** - Secure your API
   - API key authentication
   - Public vs protected endpoints
   - Authorization patterns

### Built-in Features

1. **[Built-in Endpoints](builtin-endpoints.md)** - Understand what's included
   - Health checks
   - Metrics
   - Endpoint discovery
   - Authentication endpoints

2. **[Configurable Endpoints](configurable-endpoints.md)** - Master the configuration system
   - Endpoint configuration format
   - Parameter mapping
   - Service registration
   - Advanced patterns

## Apiary Architecture

Understanding Apiary's architecture will help you make the most of its features.

### Core Components

```text
┌─────────────────────────────────────────┐
│           FastAPI Application           │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐    ┌────────▼────────┐
│  Code-based    │    │ Config-based    │
│  Routers       │    │ Endpoints       │
└───────┬────────┘    └────────┬────────┘
        │                      │
        │        ┌─────────────┘
        │        │
┌───────▼────────▼────────┐
│      Services           │
│  (Business Logic)       │
└─────────────────────────┘
        │
┌───────▼────────────────┐
│  External APIs /       │
│  Databases / etc.      │
└────────────────────────┘
```

### Request Flow

1. **Request arrives** at FastAPI
2. **Middleware processes** request (logging, rate limiting, validation)
3. **Router dispatches** to appropriate handler
4. **Service executes** business logic
5. **Response returned** with proper formatting

### Key Principles

#### 1. Separation of Concerns

- **Routers**: Handle HTTP requests/responses
- **Services**: Contain business logic
- **Models**: Define data structures
- **Middleware**: Cross-cutting concerns

#### 2. Dependency Injection

Everything uses FastAPI's dependency injection:

```python
@router.get("/endpoint")
async def endpoint(
    client: httpx.AsyncClient = Depends(http_client_dependency),
    settings: Settings = Depends(get_settings),
):
    # Use injected dependencies
    pass
```

#### 3. Configuration-Driven

Much of the behavior can be controlled via configuration:

- Endpoints can be added without code
- Features can be enabled/disabled
- Rate limits are configurable
- Services are pluggable

## Two Approaches to Endpoints

Apiary supports two ways to create endpoints. Choose based on your needs:

### Code-Based Endpoints

**Best for:**

- Complex logic
- Custom validation
- Special error handling
- Direct control

**Example:**

```python
@router.get("/complex")
async def complex_endpoint(
    param: str,
    client: httpx.AsyncClient = Depends(http_client_dependency),
):
    # Complex custom logic
    result = await do_something_complex()
    return result
```

### Configuration-Based Endpoints

**Best for:**

- Simple service calls
- Rapid prototyping
- Enabling/disabling features
- No code deployments

**Example:**

```json
{
  "path": "/api/crypto",
  "method": "GET",
  "service": "crypto",
  "enabled": true
}
```

## Common Patterns

### Public Endpoint

Accessible without authentication:

```python
@router.get("/public")
async def public_endpoint():
    return {"message": "Public data"}
```

Or in configuration:

```json
{
  "path": "/api/public",
  "requires_auth": false
}
```

### Protected Endpoint

Requires API key:

```python
@router.get("/protected")
async def protected_endpoint(
    user: AuthenticatedUser = Depends(require_auth)
):
    return {"message": "Protected data"}
```

Or in configuration:

```json
{
  "path": "/api/protected",
  "requires_auth": true
}
```

### Cached Endpoint

Add caching to reduce load:

```python
from core.cache import add_cache_headers

@router.get("/cached")
async def cached_endpoint(response: Response):
    data = expensive_operation()
    add_cache_headers(response, ttl=60)  # Cache 60s
    return data
```

### Aggregation Endpoint

Combine multiple services:

```python
@router.get("/combined")
async def combined_endpoint(
    client: httpx.AsyncClient = Depends(http_client_dependency)
):
    crypto = await crypto_service.call()
    weather = await weather_service.call()

    return {
        "crypto": crypto,
        "weather": weather
    }
```

## Development Workflow

### 1. Plan Your API

- Define endpoints
- Identify services needed
- Determine auth requirements

### 2. Create Services

- Implement business logic
- Use `BaseService` for configurable services
- Add error handling
- Write unit tests

### 3. Add Endpoints

Choose your approach:

- **Simple**: Use configuration
- **Complex**: Write code-based endpoints

### 4. Configure

- Set up `settings.json`
- Configure `endpoints.json`
- Set rate limits
- Define API keys

### 5. Test

- Run unit tests
- Test endpoints with curl
- Check metrics
- Verify health checks

### 6. Deploy

- Configure production settings
- Set up nginx
- Configure systemd
- Monitor metrics

## Best Practices

### Service Design

1. **Keep services focused** - One responsibility per service
2. **Use dependency injection** - Don't create clients in services
3. **Handle errors properly** - Use custom exceptions
4. **Make services async** - Use async/await for I/O

### Error Handling

1. **Use custom exceptions** - from `core.exceptions`
2. **Include helpful messages** - For debugging
3. **Log errors** - With appropriate log levels
4. **Return proper status codes** - 400, 404, 500, etc.

### Configuration

1. **Use settings.json** - For sensitive data
2. **Use environment variables** - For deployment
3. **Validate on startup** - Fail fast with clear errors
4. **Document settings** - So others know what to configure

### Security

1. **Use strong API keys** - Random, long strings
2. **Enable rate limiting** - Prevent abuse
3. **Validate input** - Use Pydantic models
4. **Log security events** - Authentication failures, etc.

### Performance

1. **Enable caching** - For expensive operations
2. **Use connection pooling** - Reuse HTTP connections
3. **Monitor metrics** - Track slow endpoints
4. **Optimize hot paths** - Profile and improve

## Where to Go From Here

### Beginner Path

1. [Adding Endpoints](adding-endpoints.md) - Start here
2. [Creating Services](creating-services.md) - Build logic
3. [Built-in Endpoints](builtin-endpoints.md) - Use what's included
4. [Quick Start](../getting-started/quickstart.md) - Hands-on tutorial

### Intermediate Path

1. [Authentication](authentication.md) - Secure your API
2. [Configurable Endpoints](configurable-endpoints.md) - Master configuration
3. [Development Setup](../development/setup.md) - Set up tools
4. [Testing](../development/testing.md) - Write tests

### Advanced Path

1. [Core Modules](../reference/core.md) - Deep dive
2. [Deployment](../deployment/overview.md) - Go to production
3. [Monitoring](../deployment/monitoring.md) - Track performance
4. Extend the framework - Build custom middleware

## Getting Help

- **Documentation**: You're reading it!
- **Examples**: Check `examples/` directory
- **API Docs**: Visit `/docs` on your running server
- **GitHub**: [Issues](https://github.com/lancereinsmith/apiary/issues) and [Discussions](https://github.com/lancereinsmith/apiary/discussions)

## Quick Reference

### Common Commands

```bash
# Start server
python main.py

# Run tests
pytest

# Check health
curl http://localhost:8000/health

# View metrics
curl http://localhost:8000/metrics

# List endpoints
curl http://localhost:8000/endpoints
```

### Common Imports

```python
# Services
from core.services.base import BaseService

# Auth
from core.auth.authorization import require_auth
from core.auth.authentication import AuthenticatedUser

# Exceptions
from core import ValidationError, NotFoundError, AuthenticationError

# Dependencies
from core.dependencies import http_client_dependency, get_settings

# Caching
from core.cache import add_cache_headers
```

### Configuration Templates

```json
// settings.json
{
  "api_keys": "key1,key2",
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60
}

// config/endpoints.json
{
  "endpoints": [
    {
      "path": "/api/endpoint",
      "method": "GET",
      "service": "myservice",
      "enabled": true,
      "requires_auth": false
    }
  ]
}
```

Ready to dive in? Start with [Adding Endpoints](adding-endpoints.md)!

