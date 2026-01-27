# Authentication

Learn how to implement authentication and authorization in your Apiary API.

## Overview

Apiary uses API key authentication via the `X-API-Key` header.

## Configuration

Apiary supports two types of API key configuration:

1. **Global API Keys** - Apply to all authenticated endpoints by default
2. **Endpoint-Specific API Keys** - Override global keys for specific endpoints

Both support either inline keys or loading from files.

### Global API Keys

Edit `config/settings.json`:

```json
{
  "api_keys": "key1,key2,key3"
}
```

Multiple keys can be comma-separated. Each key can represent a different client or user.

#### Using a Key File

Instead of inline keys, you can specify a file path:

```json
{
  "api_keys": "config/api_keys.txt"
}
```

The file should contain one key per line:

```text
key1
key2
key3
# Comments start with #
```

!!! tip "Auto-Reload"
    API key files are monitored for changes and automatically reloaded when modified. No server restart needed!

### Endpoint-Specific API Keys

Override global keys for specific endpoints in `config/endpoints.json`:

```json
{
  "endpoints": [
    {
      "path": "/api/admin",
      "method": "GET",
      "service": "admin",
      "enabled": true,
      "requires_auth": true,
      "api_keys": "admin-key-1,admin-key-2"
    },
    {
      "path": "/api/premium",
      "method": "GET",
      "service": "premium",
      "enabled": true,
      "requires_auth": true,
      "api_keys": "config/premium_keys.txt"
    }
  ]
}
```

When `api_keys` is specified for an endpoint:

- Only those keys can access that endpoint
- Global keys are ignored for that endpoint

### Generating Secure Keys

Generate strong random keys:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Example output: `xvT5_3kP9mN2wQ8rL6hJ4fD1sA7yU0bC5eK9nM3pR2t`

## Using Authentication

### Making Authenticated Requests

Include the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-key-here" http://localhost:8000/auth/status
```

### In Python

```python
import httpx

headers = {"X-API-Key": "your-key-here"}
response = httpx.get("http://localhost:8000/auth/status", headers=headers)
print(response.json())
```

### In JavaScript

```javascript
fetch('http://localhost:8000/auth/status', {
  headers: {
    'X-API-Key': 'your-key-here'
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

## Protecting Endpoints

### Code-Based Endpoints

Use the `require_auth` dependency:

```python
from fastapi import Depends
from core.auth.authorization import require_auth
from core.auth.authentication import AuthenticatedUser

@router.get("/protected")
async def protected_endpoint(
    user: AuthenticatedUser = Depends(require_auth)
):
    """Protected endpoint requiring API key."""
    return {
        "message": "You are authenticated",
        "api_key": user.api_key,
    }
```

### Configuration-Based Endpoints

Set `requires_auth: true`:

```json
{
  "path": "/api/protected",
  "method": "GET",
  "service": "myservice",
  "enabled": true,
  "requires_auth": true
}
```

With endpoint-specific keys:

```json
{
  "path": "/api/admin",
  "method": "GET",
  "service": "admin",
  "enabled": true,
  "requires_auth": true,
  "api_keys": "admin-key-only"
}
```

## Built-in Auth Endpoints

### Check Authentication Status

```bash
# Requires authentication
curl -H "X-API-Key: your-key" http://localhost:8000/auth/status
```

Response:

```json
{
  "authenticated": true,
  "api_key": "your-key"
}
```

### Validate API Key

```bash
# Optional authentication
curl -H "X-API-Key: your-key" http://localhost:8000/auth/validate
```

Response:

```json
{
  "authenticated": true,
  "valid": true
}
```

## Rate Limiting

Rate limiting can be based on authentication:

```json
{
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,                    // Public
  "rate_limit_per_minute_authenticated": 300      // Authenticated
}
```

## Security Considerations

### HTTPS in Production

Always use HTTPS in production to protect API keys in transit.

## Validation

Always validate your API key configuration:

```bash
uv run apiary validate-config
```
See [API Key Validation](api-key-validation.md) for details.

## Next Steps

- [API Key Validation](api-key-validation.md) - Troubleshoot configuration issues
- [Built-in Endpoints](builtin-endpoints.md) - Explore auth endpoints
- [Adding Endpoints](adding-endpoints.md) - Create protected endpoints
- [Deployment](../deployment/overview.md) - Production security
