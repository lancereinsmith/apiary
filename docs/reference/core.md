# Core Modules Reference

Reference documentation for Apiary's core modules.

## Authentication

### `core.auth.authentication`

```python
from core.auth.authentication import verify_api_key, AuthenticatedUser

# Verify API key
user = await verify_api_key(api_key="key", settings=settings)
```

### `core.auth.authorization`

```python
from core.auth.authorization import require_auth

# Protect endpoint
@router.get("/protected")
async def protected(user: AuthenticatedUser = Depends(require_auth)):
    return {"authenticated": True}
```

## Exceptions

### `core.exceptions`

```python
from core import ValidationError, NotFoundError, AuthenticationError

# Raise exceptions
raise ValidationError("Invalid input")
raise NotFoundError("Resource not found")
raise AuthenticationError("Invalid API key")
```

## Services

### `core.services.base`

```python
from core.services.base import BaseService

class MyService(BaseService):
    async def call(self, parameters=None):
        return {"result": "data"}
```

## Caching

### `core.cache`

```python
from core.cache import add_cache_headers

@router.get("/cached")
async def cached(response: Response):
    add_cache_headers(response, ttl=60)
    return {"data": "cached"}
```

## Dependencies

### `core.dependencies`

```python
from core.dependencies import http_client_dependency, get_settings

@router.get("/endpoint")
async def endpoint(
    client: httpx.AsyncClient = Depends(http_client_dependency),
    settings: Settings = Depends(get_settings),
):
    pass
```

## Next Steps

- [Services Reference](services.md)
- [Models Reference](models.md)
- [Configuration Reference](config.md)

