# Configuration

Learn how to configure Apiary for your needs.

## Configuration Files

Apiary uses two main configuration files:

1. **`settings.json`** - Application settings (API keys, rate limits, etc.)
2. **`config/endpoints.json`** - Endpoint definitions

Both files are ignored by git (via `.gitignore`) to keep sensitive data secure.

## Application Settings (`settings.json`)

### Creating Settings File

Copy the template to create your settings file:

```bash
cp settings_template.json settings.json
```

### Settings Structure

```json
{
  "api_keys": "key1,key2,key3",
  "enable_landing_page": true,
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,
  "rate_limit_per_minute_authenticated": 300
}
```

### Configuration Options

#### `api_keys`

Comma-separated list of valid API keys for authentication.

```json
{
  "api_keys": "secret-key-1,secret-key-2,secret-key-3"
}
```

- **Type**: String (comma-separated)
- **Default**: Empty string (no authentication)
- **Example**: `"key1,key2,key3"`

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

#### `rate_limit_enabled`

Enable or disable rate limiting globally.

```json
{
  "rate_limit_enabled": true
}
```

- **Type**: Boolean
- **Default**: `false`
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

Environment variables take precedence over `settings.json`.

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
      "tags": ["example"],
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
  "tags": ["crypto"],
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

Configuration is loaded in this order (later overrides earlier):

1. Default values in code
2. `settings.json` file
3. Environment variables

### Configuration Validation

Apiary validates configuration on startup:

- ✅ Valid JSON syntax
- ✅ Required fields present
- ✅ Valid types (strings, booleans, integers)
- ✅ Service names are registered
- ✅ Endpoint paths start with `/`
- ✅ HTTP methods are valid

If validation fails, the application will not start and will show an error message.

### Reloading Configuration

Configuration is loaded once at startup. To apply changes:

```bash
# Restart the server
# Press Ctrl+C to stop, then:
uv run apiary serve --reload
```

For development, use auto-reload:

```bash
uvicorn app:api --reload
# Or: uv run apiary serve --reload
```

## Advanced Configuration

### Using Environment Files

Create a `.env` file for environment variables:

```bash
# .env
API_KEYS=key1,key2,key3
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
```

Load with:

```bash
# Using python-dotenv
pip install python-dotenv

# Add to app.py (in create_app function)
from dotenv import load_dotenv
load_dotenv()
```

### Configuration Inheritance

You can have multiple configuration files for different environments:

```bash
settings.json           # Base settings
settings.dev.json       # Development overrides
settings.prod.json      # Production overrides
```

### Programmatic Configuration

Override settings in code:

```python
from config import Settings

# Create custom settings
settings = Settings(
    api_keys="custom-key",
    rate_limit_enabled=True
)
```

## Security Best Practices

### Protecting Sensitive Data

1. **Never commit** `settings.json` to version control
2. **Use strong API keys** (32+ characters, random)
3. **Rotate keys regularly** in production
4. **Use environment variables** for CI/CD
5. **Restrict file permissions**: `chmod 600 settings.json`

### API Key Management

```bash
# Generate strong random key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Multiple keys for different clients
{
  "api_keys": "client1-key,client2-key,admin-key"
}
```

### Rate Limiting

```json
{
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,         // Public: 60 req/min
  "rate_limit_per_minute_authenticated": 300  // Authenticated: 300 req/min
}
```

## Configuration Reference

See [Configuration Options Reference](../reference/config.md) for complete details on all configuration options.

## Next Steps

- [Adding Endpoints](../guide/adding-endpoints.md) - Learn to create endpoints
- [Authentication](../guide/authentication.md) - Implement auth patterns
- [Deployment Configuration](../deployment/configuration.md) - Production settings
