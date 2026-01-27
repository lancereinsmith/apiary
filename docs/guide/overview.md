# User Guide Overview

Welcome to the Apiary User Guide! This guide covers everything you need to know to build production-ready APIs with Apiary.

## What You'll Learn

This guide is organized into the following sections:

### Core Concepts

1. **[Adding Endpoints](adding-endpoints.md)** - Learn how to create API endpoints
    - Code-based endpoints (traditional FastAPI)
    - Configuration-based endpoints (Apiary's unique feature)

2. **[Creating Services](creating-services.md)** - Build reusable business logic
    - Service architecture
    - Base service interface

3. **[Authentication](authentication.md)** - Secure your API
    - API key authentication
    - Public vs protected endpoints

### Built-in Features

1. **[Built-in Endpoints](builtin-endpoints.md)** - Understand what's included
    - Health checks
    - Metrics
    - Endpoint discovery
    - Authentication endpoints

2. **[API Key Validation](api-key-validation.md)** - Validate and manage API keys
    - Configuration validation
    - Key file management / Hot-reloading keys

3. **[Advanced Configuration](advanced-configuration.md)** - Master configuration techniques
    - Environment files
    - Update-safe deployment
    - Per-endpoint configuration

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

## Where to Go From Here

### Beginner Path

1. [Adding Endpoints](adding-endpoints.md) - Start here
2. [Creating Services](creating-services.md) - Build logic
3. [Built-in Endpoints](builtin-endpoints.md) - Use what's included
4. [Quick Start](../getting-started/quickstart.md) - Hands-on tutorial

### Intermediate Path

1. [Authentication](authentication.md) - Secure your API
2. [Advanced Endpoints](advanced-endpoints.md) - Master advanced patterns
3. [Advanced Configuration](advanced-configuration.md) - Environment files and security

### Advanced Path

1. [Advanced Configuration](advanced-configuration.md) - Master configuration patterns
2. [Core Modules](../reference/core.md) - Deep dive
3. [Deployment](../deployment/overview.md) - Go to production
4. [Monitoring](../deployment/monitoring.md) - Track performance

Ready to dive in? Continue with [Adding Endpoints](adding-endpoints.md)!
