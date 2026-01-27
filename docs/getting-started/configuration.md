# Configuration

Learn how to configure Apiary for your needs.

## Configuration Files

Apiary uses two main configuration files:

1. **`config/settings.json`** - Application settings (API keys, rate limits, etc.)
2. **`config/endpoints.json`** - Endpoint definitions

Both files are ignored by git (via `.gitignore`) to keep sensitive data secure and prevent merge conflicts during updates.

## Application Settings (`config/settings.json`)

### Creating Settings File

Use the CLI to initialize configuration files:

```bash
uv run apiary init
```

Or manually copy the template:

```bash
cp config/settings_template.json config/settings.json
```

### Settings Structure

```json
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
```

### Configuration Options

#### `api_keys`

Comma-separated list of valid API keys for authentication, or a path to a file containing keys.

```json
{
  "api_keys": "secret-key-1,secret-key-2,secret-key-3"
}
```

Or use a file:

```json
{
  "api_keys": "config/api_keys.txt"
}
```

- **Type**: String (comma-separated keys or file path)
- **Default**: Empty string (no authentication)
- **Example**: `"key1,key2,key3"` or `"config/api_keys.txt"`

!!! tip "Using Key Files"
    Key files should contain one key per line. Comments starting with `#` are ignored.
    Files are automatically monitored and reloaded when changed.

    ```text
    # config/api_keys.txt
    key1
    key2
    key3
    ```

!!! tip "Generating API Keys"
    Generate strong random API keys:

    ```bash
    python -c "import secrets; print(secrets.token_urlsafe(32))"
    ```

#### `enable_landing_page`

Enable or disable the HTML landing page at `/`.

```json
{
  "enable_landing_page": true
}
```

- **Type**: Boolean
- **Default**: `true`
- **Values**: `true` (enabled), `false` (disabled)

#### `enable_docs`

Enable or disable the interactive Swagger UI documentation at `/docs`.

```json
{
  "enable_docs": true
}
```

- **Type**: Boolean
- **Default**: `true`
- **Values**: `true` (enabled), `false` (disabled)

!!! info "API Documentation"
    The Swagger UI provides an interactive interface to explore and test your API endpoints.
    Disable this in production if you don't want to expose API documentation publicly.

#### `enable_redoc`

Enable or disable the ReDoc documentation interface at `/redoc`.

```json
{
  "enable_redoc": true
}
```

- **Type**: Boolean
- **Default**: `true`
- **Values**: `true` (enabled), `false` (disabled)

!!! info "Alternative Documentation"
    ReDoc provides a clean, responsive alternative to Swagger UI for viewing API documentation.
    It's read-only and optimized for documentation browsing.

#### `enable_openapi`

Enable or disable the OpenAPI schema endpoint at `/openapi.json`.

```json
{
  "enable_openapi": true
}
```

- **Type**: Boolean
- **Default**: `true`
- **Values**: `true` (enabled), `false` (disabled)

!!! info "OpenAPI Schema"
    The OpenAPI schema can be used by API clients, code generators, and testing tools.
    Disable this if you want to keep your API schema private.

#### `enabled_routers`

List of routers to enable. This allows you to selectively enable or disable API
features without modifying code.

```json
{
  "enabled_routers": ["health", "metrics", "auth", "endpoints"]
}
```

- **Type**: Array of strings
- **Default**: `["health", "metrics", "auth", "endpoints"]`
- **Built-in routers**:
    - `health` - Health check endpoints
    - `metrics` - Application metrics endpoints
    - `auth` - Authentication endpoints (login, token validation)
    - `endpoints` - List available endpoints

!!! example "Disable Authentication"
    To run without authentication endpoints:

    ```json
    {
      "enabled_routers": ["health", "metrics", "endpoints"]
    }
    ```

!!! tip "Custom Routers"
    Routers are automatically discovered from the `routers/` directory. Simply create a router file (e.g., `routers/example.py`) and add its name to `enabled_routers`. See [Adding Endpoints](../guide/adding-endpoints.md) for details.

#### `rate_limit_enabled`

Enable or disable rate limiting globally.

```json
{
  "rate_limit_enabled": true
}
```

- **Type**: Boolean
- **Default**: `true`
- **Values**: `true` (enabled), `false` (disabled)

#### `rate_limit_per_minute`

Rate limit for unauthenticated requests (requests per minute per IP).

```json
{
  "rate_limit_per_minute": 60
}
```

- **Type**: Integer
- **Default**: `60`
- **Example**: `60` (60 requests per minute)

#### `rate_limit_per_minute_authenticated`

Rate limit for authenticated requests (requests per minute per API key).

```json
{
  "rate_limit_per_minute_authenticated": 300
}
```

- **Type**: Integer
- **Default**: `300`
- **Example**: `300` (300 requests per minute)

### Environment Variables

Settings can be overridden with environment variables:

```bash
export API_KEYS="key1,key2"
export RATE_LIMIT_ENABLED=true
export RATE_LIMIT_PER_MINUTE=100
export RATE_LIMIT_PER_MINUTE_AUTHENTICATED=500

uv run apiary serve --reload
```

Environment variables take precedence over `config/settings.json`.

### Example Configurations

#### Development

```json
{
  "api_keys": "dev-key-123",
  "enable_landing_page": true,
  "rate_limit_enabled": false
}
```

#### Production

```json
{
  "api_keys": "prod-key-a1b2c3d4,prod-key-e5f6g7h8",
  "enable_landing_page": true,
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,
  "rate_limit_per_minute_authenticated": 300
}
```

#### Testing

```json
{
  "api_keys": "test-key",
  "enable_landing_page": false,
  "rate_limit_enabled": false
}
```

## Endpoint Configuration (`config/endpoints.json`)

### Creating Endpoints File

Copy the template:

```bash
cp config/endpoints_template.json config/endpoints.json
```

### Endpoint Structure

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
      "tags": [
        "example"
      ],
      "summary": "Example endpoint",
      "parameters": {
        "param1": {
          "source": "query",
          "key": "param1"
        }
      }
    }
  ]
}
```

### Endpoint Options

#### `path`

The URL path for the endpoint.

- **Type**: String
- **Required**: Yes
- **Example**: `"/api/crypto"`, `"/api/hello"`
- **Must start with**: `/`

#### `method`

HTTP method for the endpoint.

- **Type**: String
- **Required**: Yes
- **Values**: `"GET"`, `"POST"`, `"PUT"`, `"DELETE"`, `"PATCH"`
- **Example**: `"GET"`

#### `service`

Name of the service to call (must be registered).

- **Type**: String
- **Required**: Yes
- **Example**: `"crypto"`, `"hello"`

#### `enabled`

Enable or disable the endpoint.

- **Type**: Boolean
- **Required**: Yes
- **Values**: `true` (enabled), `false` (disabled)
- **Example**: `true`

#### `requires_auth`

Whether authentication is required.

- **Type**: Boolean
- **Required**: Yes
- **Values**: `true` (protected), `false` (public)
- **Example**: `false`

#### `description`

Detailed description for API documentation.

- **Type**: String
- **Required**: No
- **Example**: `"Get cryptocurrency price data. Accepts optional 'symbol' parameter."`

#### `tags`

OpenAPI tags for grouping endpoints.

- **Type**: Array of strings
- **Required**: No
- **Example**: `["crypto", "finance"]`

#### `summary`

Short summary for API documentation.

- **Type**: String
- **Required**: No
- **Example**: `"Cryptocurrency prices"`

#### `parameters`

Parameter mapping from request to service.

- **Type**: Object
- **Required**: No

Parameter mapping types:

```json
{
  "parameters": {
    "static_value": "hardcoded-value",
    "from_query": {
      "source": "query",
      "key": "q"
    },
    "from_path": {
      "source": "path",
      "key": "id"
    }
  }
}
```

### Example Configurations

#### Simple Public Endpoint

```json
{
  "path": "/api/crypto",
  "method": "GET",
  "service": "crypto",
  "enabled": true,
  "requires_auth": false,
  "description": "Get cryptocurrency prices",
  "tags": ["crypto"]
}
```

#### Protected Endpoint

```json
{
  "path": "/api/admin/stats",
  "method": "GET",
  "service": "stats",
  "enabled": true,
  "requires_auth": true,
  "description": "Admin statistics (requires API key)",
  "tags": ["admin"]
}
```

#### Endpoint with Parameters

```json
{
    "path": "/api/crypto",
    "method": "GET",
    "service": "crypto",
    "enabled": true,
    "requires_auth": false,
    "description": "Get crypto price by symbol",
    "tags": [
        "crypto"
    ],
    "parameters": {
        "symbol": {
            "source": "query",
            "key": "symbol"
        }
    }
}
```

#### Disabled Endpoint

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

## Loading Configuration

### Priority Order

Configuration is loaded in this order (higher numbers override lower):

1. Default values in code
2. `config/settings.json` file
3. Environment variables

### Configuration Validation

Apiary validates configuration on startup:

- Valid JSON syntax
- Required fields present
- Service names are registered
- Endpoint paths start with `/`
- HTTP methods are valid

If validation fails, the application will not start and will show an error message.

### Reloading Configuration

Configuration is loaded once at startup. To apply changes, restart the server:

```bash

## Press Ctrl+C to stop, then

uv run apiary serve --reload
```

## Advanced Topics

For advanced configuration including environment files, update-safe deployment patterns, security best practices, and per-endpoint configuration, see:

- [Advanced Configuration](../guide/advanced-configuration.md) - Environment files, configuration inheritance, security
- [Configuration Options Reference](../reference/config.md) - Complete configuration reference

## Next Steps

- [Adding Endpoints](../guide/adding-endpoints.md) - Learn to create endpoints
- [Authentication](../guide/authentication.md) - Implement auth patterns
- [Deployment Configuration](../deployment/configuration.md) - Production settings
