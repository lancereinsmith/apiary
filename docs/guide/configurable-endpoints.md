# Configurable Endpoints

Master Apiary's configuration-driven endpoint system to add and manage endpoints without code changes.

## Overview

Configurable endpoints allow you to:

- ✅ Add endpoints via JSON configuration
- ✅ Enable/disable endpoints without deployment
- ✅ Rapid prototyping and iteration
- ✅ Non-technical endpoint management
- ✅ Consistent endpoint patterns

## Configuration File

Endpoints are defined in `config/endpoints.json`:

```json
{
  "endpoints": [
    {
      "path": "/api/example",
      "method": "GET",
      "service": "example",
      "enabled": true,
      "requires_auth": false,
      "description": "Example endpoint",
      "tags": ["example"]
    }
  ]
}
```

## Complete Configuration Options

```json
{
  "path": "/api/endpoint",
  "method": "GET",
  "service": "myservice",
  "enabled": true,
  "requires_auth": false,
  "description": "Detailed description for API docs",
  "tags": ["category"],
  "summary": "Short summary",
  "parameters": {
    "param1": "static-value",
    "param2": {
      "source": "query",
      "key": "q"
    }
  }
}
```

## Parameter Mapping

### Static Values

```json
{
  "parameters": {
    "version": "v1",
    "source": "api"
  }
}
```

### Query Parameters

```json
{
  "parameters": {
    "city": {
      "source": "query",
      "key": "city"
    }
  }
}
```

Usage: `GET /api/weather?city=London`

### Path Parameters

```json
{
  "path": "/api/user/{id}",
  "parameters": {
    "user_id": {
      "source": "path",
      "key": "id"
    }
  }
}
```

Usage: `GET /api/user/123`

### Mixed Parameters

```json
{
  "path": "/api/search/{category}",
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
    }
  }
}
```

Usage: `GET /api/search/books?q=python&limit=10`

## Complete Examples

### Public Endpoint

```json
{
  "path": "/api/crypto",
  "method": "GET",
  "service": "crypto",
  "enabled": true,
  "requires_auth": false,
  "description": "Get cryptocurrency price data. Accepts optional 'symbol' parameter (e.g., BTC, ETH, SOL).",
  "tags": ["crypto"],
  "summary": "Cryptocurrency prices",
  "parameters": {
    "symbol": {
      "source": "query",
      "key": "symbol"
    }
  }
}
```

### Protected Endpoint

```json
{
  "path": "/api/admin/users",
  "method": "GET",
  "service": "admin_users",
  "enabled": true,
  "requires_auth": true,
  "description": "List all users (requires authentication)",
  "tags": ["admin"],
  "summary": "List users"
}
```

### Disabled Endpoint

```json
{
  "path": "/api/beta-feature",
  "method": "GET",
  "service": "beta",
  "enabled": false,
  "requires_auth": false,
  "description": "Beta feature (currently disabled)"
}
```

## Endpoint Discovery

List all configured endpoints:

```bash
curl http://localhost:8000/endpoints
```

Response shows all endpoints, their configuration, and available services.

## Best Practices

### 1. Use Clear Paths

```json
// Good
{"path": "/api/crypto"}
{"path": "/api/weather/current"}

// Avoid
{"path": "/c"}
{"path": "/api/get_crypto_data"}
```

### 2. Add Descriptions

```json
{
  "description": "Get cryptocurrency price data. Accepts optional 'symbol' parameter (e.g., BTC, ETH, SOL). Defaults to BTC if not provided.",
  "summary": "Cryptocurrency prices"
}
```

### 3. Use Tags for Organization

```json
{
  "tags": ["crypto", "finance"]
}
```

### 4. Document Parameters

```json
{
  "description": "Search books. Parameters: 'q' (query string), 'limit' (max results, default 10)",
  "parameters": {
    "query": {"source": "query", "key": "q"},
    "limit": {"source": "query", "key": "limit"}
  }
}
```

### 5. Version Your APIs

```json
{
  "path": "/api/v1/crypto"
}
```

## Troubleshooting

### Endpoint Not Appearing

1. Check JSON syntax: `python -m json.tool config/endpoints.json`
2. Verify service is registered
3. Ensure `enabled: true`
4. Restart the server
5. Check logs for errors

### Service Not Found

1. Verify service registration in `services/__init__.py`
2. Check service name matches exactly
3. Ensure service inherits from `BaseService`

### Parameters Not Working

1. Verify parameter mapping syntax
2. Check source type (query/path)
3. Ensure keys match exactly
4. Test with curl to isolate issues

## Next Steps

- [Creating Services](creating-services.md) - Build services for your endpoints
- [Adding Endpoints](adding-endpoints.md) - Learn code-based approach too
- [Configuration](../getting-started/configuration.md) - Master configuration

