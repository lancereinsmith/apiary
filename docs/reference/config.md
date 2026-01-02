# Configuration Reference

Complete reference for all configuration options.

## Application Settings (`settings.json`)

### `api_keys`

Comma-separated list of valid API keys.

- **Type**: String
- **Default**: `""`
- **Example**: `"key1,key2,key3"`

### `enable_landing_page`

Enable/disable HTML landing page.

- **Type**: Boolean
- **Default**: `true`

### `rate_limit_enabled`

Enable/disable rate limiting.

- **Type**: Boolean
- **Default**: `false`

### `rate_limit_per_minute`

Rate limit for unauthenticated requests.

- **Type**: Integer
- **Default**: `60`

### `rate_limit_per_minute_authenticated`

Rate limit for authenticated requests.

- **Type**: Integer
- **Default**: `300`

## Endpoint Configuration (`config/endpoints.json`)

### `path`

URL path for endpoint (must start with `/`).

- **Type**: String
- **Required**: Yes

### `method`

HTTP method.

- **Type**: String
- **Values**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- **Required**: Yes

### `service`

Service name (must be registered).

- **Type**: String
- **Required**: Yes

### `enabled`

Enable/disable endpoint.

- **Type**: Boolean
- **Required**: Yes

### `requires_auth`

Require authentication.

- **Type**: Boolean
- **Required**: Yes

### `description`

Detailed description for API docs.

- **Type**: String
- **Required**: No

### `tags`

OpenAPI tags for grouping.

- **Type**: Array of strings
- **Required**: No

### `summary`

Short summary for API docs.

- **Type**: String
- **Required**: No

### `parameters`

Parameter mapping.

- **Type**: Object
- **Required**: No

## Next Steps

- [Configuration Guide](../getting-started/configuration.md)
- [Configurable Endpoints](../guide/configurable-endpoints.md)

