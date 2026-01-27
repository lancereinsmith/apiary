# Quick Reference

## Common Commands

```bash
# Start server
uv run apiary serve --reload
# Or: uvicorn app:api --reload

# Run tests
pytest

# Check health
curl http://localhost:8000/health

# View metrics
curl http://localhost:8000/metrics

# List endpoints
curl http://localhost:8000/endpoints
```

## Common Imports

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

## Configuration Templates

```json
// config/settings.json
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

// config/endpoints.json
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

## Next Steps

- [Configuration Guide](../getting-started/configuration.md)
- [Adding Endpoints](../guide/adding-endpoints.md)
- [API Key Validation Guide](../guide/api-key-validation.md)
