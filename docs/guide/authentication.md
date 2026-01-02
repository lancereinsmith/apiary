# Authentication

Learn how to implement authentication and authorization in your Apiary API.

## Overview

Apiary uses API key authentication via the `X-API-Key` header. This provides:

- ✅ Simple implementation
- ✅ No session management
- ✅ Stateless authentication
- ✅ Easy to test
- ✅ Per-endpoint control

## Configuration

### Setting API Keys

Edit `settings.json`:

```json
{
  "api_keys": "key1,key2,key3"
}
```

Multiple keys can be comma-separated. Each key can represent a different client or user.

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

Authenticated users get higher rate limits:

```json
{
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,                    // Public
  "rate_limit_per_minute_authenticated": 300      // Authenticated
}
```

## Best Practices

### 1. Use Strong Keys

```bash
# Generate 32-byte random key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Rotate Keys Regularly

Update keys periodically in production:

```json
{
  "api_keys": "new-key-1,new-key-2,old-key-1"
}
```

Keep old keys temporarily for transition.

### 3. Different Keys for Different Clients

```json
{
  "api_keys": "mobile-app-key,web-app-key,admin-key"
}
```

### 4. Never Commit Keys

Add to `.gitignore`:

```text
settings.json
config/endpoints.json
```

### 5. Use Environment Variables in Production

```bash
export API_KEYS="prod-key-1,prod-key-2"
```

## Security Considerations

### HTTPS in Production

Always use HTTPS in production to protect API keys in transit.

### Key Storage

- ❌ Don't hardcode in client applications
- ❌ Don't commit to version control
- ✅ Use environment variables
- ✅ Use secret management services
- ✅ Restrict file permissions: `chmod 600 settings.json`

### Monitoring

Log authentication failures:

```python
logger.warning(
    "Authentication failed",
    extra={"ip": request.client.host}
)
```

## Next Steps

- [Built-in Endpoints](builtin-endpoints.md) - Explore auth endpoints
- [Adding Endpoints](adding-endpoints.md) - Create protected endpoints
- [Deployment](../deployment/overview.md) - Production security

