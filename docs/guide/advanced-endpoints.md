# Advanced Endpoint Patterns

Learn advanced patterns for building sophisticated endpoints with Apiary.

!!! info "Prerequisites"
    This guide assumes you're familiar with basic endpoint creation. If you're new to Apiary, start with [Adding Endpoints](adding-endpoints.md).

## Endpoint-Specific API Keys

Configuration-based endpoints support endpoint-specific API keys that override global keys.

### Use Cases

- **Admin endpoints** - Require special admin-only keys
- **Premium features** - Different keys for different tiers
- **Partner integrations** - Unique keys per partner
- **Testing** - Separate test keys from production

### Inline Keys

Specify API keys directly in the endpoint configuration:

```json
{
  "path": "/api/admin",
  "method": "GET",
  "service": "admin",
  "enabled": true,
  "requires_auth": true,
  "api_keys": "admin-key-1,admin-key-2",
  "description": "Admin-only endpoint",
  "tags": ["admin"]
}
```

Only `admin-key-1` and `admin-key-2` can access this endpoint. Global keys are ignored.

### File-Based Keys

Store keys in a separate file for easier management:

```json
{
  "path": "/api/premium",
  "method": "GET",
  "service": "premium",
  "enabled": true,
  "requires_auth": true,
  "api_keys": "config/premium_keys.txt",
  "description": "Premium features",
  "tags": ["premium"]
}
```

Create `config/premium_keys.txt`:

```text
# Premium tier API keys
premium-key-abc123
premium-key-def456
premium-key-ghi789
```

!!! tip "Auto-Reload"
    Key files are automatically monitored and reloaded when changed. No server restart needed!

### Mixed Configuration Example

```json
{
  "endpoints": [
    {
      "path": "/api/public",
      "method": "GET",
      "service": "public",
      "enabled": true,
      "requires_auth": false,
      "description": "Public endpoint (no auth)"
    },
    {
      "path": "/api/users",
      "method": "GET",
      "service": "users",
      "enabled": true,
      "requires_auth": true,
      "description": "User data (uses global keys)"
    },
    {
      "path": "/api/admin",
      "method": "GET",
      "service": "admin",
      "enabled": true,
      "requires_auth": true,
      "api_keys": "config/admin_keys.txt",
      "description": "Admin endpoint (admin keys only)"
    }
  ]
}
```

**Result:**

- `/api/public` - No authentication required
- `/api/users` - Uses global keys from `config/settings.json`
- `/api/admin` - Uses only keys from `config/admin_keys.txt`

### Validate Configuration

Always validate your API key configuration:

```bash
uv run apiary validate-config
```

See [API Key Validation](api-key-validation.md) for details.

## Advanced Parameter Mapping

### Mixed Parameters

Combine path, query, and static parameters:

```json
{
  "path": "/api/search/{category}",
  "method": "GET",
  "service": "search",
  "enabled": true,
  "requires_auth": false,
  "parameters": {
    "category": {
      "source": "path",
      "key": "category"
    },
    "query": {
      "source": "query",
      "key": "q"
    },
    "limit": {
      "source": "query",
      "key": "limit"
    },
    "version": "v1"
  }
}
```

Usage: `GET /api/search/books?q=python&limit=10`

The service receives:

```python
{
  "category": "books",
  "query": "python",
  "limit": "10",
  "version": "v1"
}
```

## Complete Examples

### Example 1: Protected Admin Endpoint

Code-based approach with global keys:

```python
@router.get("/admin/stats")
async def admin_stats(
    user: AuthenticatedUser = Depends(require_auth),
):
    """Admin statistics endpoint."""
    return {
        "total_requests": get_total_requests(),
        "active_users": get_active_users(),
        "system_health": get_system_health(),
    }
```

Configuration-based approach with endpoint-specific keys:

```json
{
  "path": "/api/admin/stats",
  "method": "GET",
  "service": "admin_stats",
  "enabled": true,
  "requires_auth": true,
  "api_keys": "config/admin_keys.txt",
  "description": "Admin statistics (requires admin API key)",
  "tags": ["admin"]
}
```

Create `config/admin_keys.txt`:

```text
# Admin API keys
admin-Xk9mP2vN4wQ8rL6hJ5fD1sA7yU0bC3eK
admin-yU0bC3eK9nM3pR2tXk9mP2vN4wQ8rL6h
```

Test the endpoint:

```bash
# With admin key - succeeds
curl -H "X-API-Key: admin-Xk9mP2vN4wQ8rL6hJ5fD1sA7yU0bC3eK" \
  http://localhost:8000/api/admin/stats

# With regular user key - fails
curl -H "X-API-Key: regular-user-key" \
  http://localhost:8000/api/admin/stats
```

### Example 2: Multi-Tier Access

Create different endpoints for different access tiers:

```json
{
  "endpoints": [
    {
      "path": "/api/basic",
      "method": "GET",
      "service": "basic_features",
      "enabled": true,
      "requires_auth": true,
      "description": "Basic tier features (uses global keys)"
    },
    {
      "path": "/api/premium",
      "method": "GET",
      "service": "premium_features",
      "enabled": true,
      "requires_auth": true,
      "api_keys": "config/premium_keys.txt",
      "description": "Premium tier features"
    },
    {
      "path": "/api/enterprise",
      "method": "GET",
      "service": "enterprise_features",
      "enabled": true,
      "requires_auth": true,
      "api_keys": "config/enterprise_keys.txt",
      "description": "Enterprise tier features"
    }
  ]
}
```

This creates a three-tier access system:

- **Basic** - All authenticated users (global keys)
- **Premium** - Only premium subscribers (premium_keys.txt)
- **Enterprise** - Only enterprise clients (enterprise_keys.txt)

**Key file organization:**

```text
config/
├── api_keys.txt          # Basic tier (global keys)
├── premium_keys.txt      # Premium tier
└── enterprise_keys.txt   # Enterprise tier
```

**Testing the tiers:**

```bash
# Basic tier - works with any valid key
curl -H "X-API-Key: basic-key" http://localhost:8000/api/basic

# Premium tier - only premium keys
curl -H "X-API-Key: premium-key-abc123" http://localhost:8000/api/premium

# Enterprise tier - only enterprise keys
curl -H "X-API-Key: enterprise-key-xyz789" http://localhost:8000/api/enterprise
```

## Advanced Troubleshooting

### Endpoint-Specific Authentication Issues

**For endpoint-specific keys:**

- Verify `api_keys` field in endpoint configuration
- Run `uv run apiary validate-config` to check for errors
- If using a file, ensure it exists: `ls config/your_keys.txt`
- Check file has valid keys (one per line, no commas)
- Verify you're using the correct key for that specific endpoint
- Check server logs on startup for validation warnings

### JSON Validation

Validate your endpoints.json syntax:

```bash
python -m json.tool config/endpoints.json
```

If valid, it will output the formatted JSON. If invalid, you'll see an error message.

### Key File Format Issues

Common mistakes:

```text
# ❌ Wrong - comma-separated (use this in JSON, not files)
key1,key2,key3

# ❌ Wrong - JSON format in text file
{"keys": ["key1", "key2"]}

# ✅ Correct - one key per line
key1
key2
key3
```

## Next Steps

- [API Key Examples](api-key-examples.md) - API key configuration examples
- [API Key Validation](api-key-validation.md) - Comprehensive validation guide
- [Authentication](authentication.md) - Full authentication documentation
- [Creating Services](creating-services.md) - Build robust services
