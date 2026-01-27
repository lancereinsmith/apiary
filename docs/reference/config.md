# Configuration Reference

Complete reference for all configuration options in Apiary.

## Overview

Apiary uses two main configuration files:

- **`config/settings.json`** - Application-wide settings (authentication, UI, rate limits)
- **`config/endpoints.json`** - Dynamic endpoint definitions

Both files are created from templates when you run `uv run apiary init`.

---

## Application Settings

Application settings are defined in `config/settings.json` and validated using the `Settings` Pydantic model.

::: config.settings.Settings
    options:
      show_root_heading: true
      show_source: false
      members:
        - api_keys
        - enable_landing_page
        - enable_docs
        - enable_redoc
        - enable_openapi
        - enabled_routers
        - rate_limit_enabled
        - rate_limit_per_minute
        - rate_limit_per_minute_authenticated
      show_bases: false
      heading_level: 3

### API Keys Format

The `api_keys` field supports two formats:

=== "Comma-Separated String"

    ```json
    {
      "api_keys": "key1,key2,key3"
    }
    ```

=== "File Path"

    ```json
    {
      "api_keys": "config/api_keys.txt"
    }
    ```

    File format (one key per line):

    ```text
    # Admin keys
    admin-key-1234
    admin-key-5678

    # User keys
    user-key-abcd
    ```

    - Lines starting with `#` are comments
    - Empty lines are ignored
    - File changes are automatically detected and reloaded

### Example Settings File

```json
{
  "api_keys": "config/api_keys.txt",
  "enable_landing_page": true,
  "enable_docs": true,
  "enable_redoc": true,
  "enable_openapi": true,
  "enabled_routers": ["health", "metrics", "auth", "endpoints"],
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,
  "rate_limit_per_minute_authenticated": 300
}
```

---

## Endpoint Configuration

Dynamic endpoints are defined in `config/endpoints.json` as an array of endpoint configurations. Each endpoint is validated using the `EndpointConfig` Pydantic model.

::: config.endpoint_config.EndpointConfig
    options:
      show_root_heading: true
      show_source: false
      members:
        - path
        - method
        - service
        - enabled
        - requires_auth
        - api_keys
        - description
        - tags
        - summary
        - parameters
        - response_model
      show_bases: false
      heading_level: 3

### HTTP Methods

::: config.endpoint_config.HTTPMethod
    options:
      show_root_heading: true
      show_source: false
      heading_level: 4

### Endpoint-Specific API Keys

Individual endpoints can override global API keys by specifying an `api_keys` field. This is useful for:

- **Admin endpoints** - Require specific admin keys
- **Premium features** - Use separate keys for paid features
- **Partner integrations** - Different keys for different partners

When `api_keys` is specified on an endpoint, **only those keys are valid** for that endpoint (global keys are ignored).

### Example Endpoint Configurations

=== "Basic Endpoint"

    ```json
    {
      "path": "/api/hello",
      "method": "GET",
      "service": "hello",
      "enabled": true,
      "requires_auth": false,
      "description": "Simple hello world endpoint",
      "tags": ["demo"]
    }
    ```

=== "Authenticated Endpoint"

    ```json
    {
      "path": "/api/crypto",
      "method": "GET",
      "service": "crypto",
      "enabled": true,
      "requires_auth": true,
      "description": "Get cryptocurrency price data",
      "tags": ["crypto"],
      "parameters": {
        "symbol": "BTC"
      }
    }
    ```

=== "Endpoint-Specific Keys"

    ```json
    {
      "path": "/api/admin",
      "method": "POST",
      "service": "admin",
      "enabled": true,
      "requires_auth": true,
      "api_keys": "admin-key-1,admin-key-2",
      "description": "Admin-only endpoint",
      "tags": ["admin"]
    }
    ```

=== "File-Based Keys"

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

### Complete Endpoints File Example

```json
{
  "endpoints": [
    {
      "path": "/api/hello",
      "method": "GET",
      "service": "hello",
      "enabled": true,
      "requires_auth": false,
      "description": "Simple greeting endpoint",
      "tags": ["demo"],
      "parameters": {
        "name": "World"
      }
    },
    {
      "path": "/api/crypto",
      "method": "GET",
      "service": "crypto",
      "enabled": true,
      "requires_auth": true,
      "description": "Cryptocurrency price data",
      "tags": ["crypto"],
      "parameters": {
        "symbol": "BTC"
      }
    }
  ]
}
```

---

## Configuration Models

### Settings Model

Full Settings model documentation:

::: config.settings.Settings
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

### Endpoint Config Model

Full EndpointConfig model documentation:

::: config.endpoint_config.EndpointConfig
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

### Endpoints Config Collection

::: config.endpoint_config.EndpointsConfig
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

---

## Validation

Configuration files are validated on startup using Pydantic. Common validation checks:

- **Path format** - Must start with `/`
- **Duplicate endpoints** - No two enabled endpoints can have the same path + method combination
- **Required fields** - All required fields must be present
- **Type checking** - Values must match expected types

Use the CLI to validate configuration before starting:

```bash
uv run apiary validate-config
```

---

## Next Steps

- [Configuration Guide](../getting-started/configuration.md) - Step-by-step configuration setup
- [Adding Endpoints](../guide/adding-endpoints.md) - How to add custom endpoints
- [API Key Validation](../guide/api-key-validation.md) - API key setup and troubleshooting
- [CLI Reference](cli.md) - Command-line tools for configuration management
