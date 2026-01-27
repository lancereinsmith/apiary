# API Key Configuration Examples

This document shows various API key configurations and their validation results.

## Example 1: Valid Configuration with Files

### config/settings.json

```json
{
  "api_keys": "config/api_keys.txt",
  "enable_landing_page": true,
  "rate_limit_enabled": true
}
```

### config/api_keys.txt

```text
# Production API keys
Xk9mP2vN4wQ8rL6hJ5fD1sA7yU0bC3eK
yU0bC3eK9nM3pR2tXk9mP2vN4wQ8rL6h
qW3eR5tY7uI9oP1aS2dF4gH6jK8lZ0xC
```

### Validation Result

```bash
$ uv run apiary validate-config
🔍 Validating API key configurations...

INFO: Validating API key configurations...
INFO: settings.api_keys: File 'config/api_keys.txt' contains 3 key(s)
INFO: ✅ All API key configurations are valid

✅ Configuration is valid
```

✅ **Result: Valid** - All keys loaded successfully

---

## Example 2: Misspelled Filename (Error Caught!)

### config/settings.json

```json
{
  "api_keys": "config/api_keyz.txt"
}
```

### Validation Result

```bash
$ uv run apiary validate-config
🔍 Validating API key configurations...

INFO: Validating API key configurations...
ERROR: settings.api_keys: File 'config/api_keyz.txt' does not exist. If this is meant to be an API key, it looks like a file path.
ERROR: ❌ API key configuration validation failed

❌ Configuration has errors (see above)
```

❌ **Result: Error** - Typo detected! Should be `api_keys.txt`, not `api_keyz.txt`

---

## Example 3: Valid Inline Keys

### config/settings.json

```json
{
  "api_keys": "Xk9mP2vN4wQ8rL6hJ5fD1sA7yU0bC3eK,yU0bC3eK9nM3pR2tXk9mP2vN4wQ8rL6h"
}
```

### Validation Result

```bash
$ uv run apiary validate-config
🔍 Validating API key configurations...

INFO: Validating API key configurations...
INFO: settings.api_keys: Contains 2 inline key(s)
INFO: ✅ All API key configurations are valid

✅ Configuration is valid
```

✅ **Result: Valid** - Inline keys are properly formatted

---

## Example 4: Weak Key Warning

### config/settings.json

```json
{
  "api_keys": "test123,abc"
}
```

### Validation Result

```bash
$ uv run apiary validate-config
🔍 Validating API key configurations...

INFO: Validating API key configurations...
WARNING: settings.api_keys: Key 'test123' is very short (less than 8 characters). Consider using stronger keys.
WARNING: settings.api_keys: Key 'abc' is very short (less than 8 characters). Consider using stronger keys.
INFO: ✅ All API key configurations are valid

✅ Configuration is valid
```

⚠️ **Result: Valid with Warnings** - Works but keys are weak

---

## Example 5: Endpoint-Specific Keys

### config/endpoints.json

```json
{
  "endpoints": [
    {
      "path": "/api/public",
      "method": "GET",
      "service": "public",
      "enabled": true,
      "requires_auth": false
    },
    {
      "path": "/api/users",
      "method": "GET",
      "service": "users",
      "enabled": true,
      "requires_auth": true
    },
    {
      "path": "/api/admin",
      "method": "GET",
      "service": "admin",
      "enabled": true,
      "requires_auth": true,
      "api_keys": "config/admin_keys.txt"
    }
  ]
}
```

### config/admin_keys.txt

```text
# Admin-only keys
admin-Xk9mP2vN4wQ8rL6hJ5fD1sA7yU0bC3eK
admin-yU0bC3eK9nM3pR2tXk9mP2vN4wQ8rL6h
```

### Validation Result

```bash
$ uv run apiary validate-config
🔍 Validating API key configurations...

INFO: Validating API key configurations...
INFO: settings.api_keys: Contains 2 inline key(s)
INFO: endpoints[/api/admin].api_keys: File 'config/admin_keys.txt' contains 2 key(s)
INFO: ✅ All API key configurations are valid

✅ Configuration is valid
```

✅ **Result: Valid**

- `/api/public` - No authentication required
- `/api/users` - Uses global keys from settings.json
- `/api/admin` - Uses specific keys from admin_keys.txt

---

## Example 6: Empty Key File

### config/api_keys.txt

```text
# All keys are commented out
# key1
# key2
# key3
```

### Validation Result

```bash
$ uv run apiary validate-config
🔍 Validating API key configurations...

INFO: Validating API key configurations...
WARNING: settings.api_keys: File 'config/api_keys.txt' contains no valid API keys
ERROR: settings.api_keys: No valid keys found in string
ERROR: ❌ API key configuration validation failed

❌ Configuration has errors (see above)
```

❌ **Result: Error** - File exists but has no valid keys

---

## Example 7: Mixed Configuration (File + Inline)

### config/settings.json

```json
{
  "api_keys": "config/global_keys.txt"
}
```

### config/endpoints.json

```json
{
  "endpoints": [
    {
      "path": "/api/premium",
      "method": "GET",
      "service": "premium",
      "enabled": true,
      "requires_auth": true,
      "api_keys": "premium-key-1,premium-key-2"
    }
  ]
}
```

### Validation Result

```bash
$ uv run apiary validate-config
🔍 Validating API key configurations...

INFO: Validating API key configurations...
INFO: settings.api_keys: File 'config/global_keys.txt' contains 5 key(s)
INFO: endpoints[/api/premium].api_keys: Contains 2 inline key(s)
INFO: ✅ All API key configurations are valid

✅ Configuration is valid
```

✅ **Result: Valid** - Can mix file and inline configurations

---

## Best Practices

### ✅ DO

```json
// Use files for production
{
  "api_keys": "config/api_keys.txt"
}

// Use strong keys
{
  "api_keys": "Xk9mP2vN4wQ8rL6hJ5fD1sA7yU0bC3eK"
}

// Endpoint-specific keys for admin endpoints
{
  "path": "/api/admin",
  "api_keys": "config/admin_keys.txt"
}
```

### ❌ DON'T

```json
// Don't use weak keys
{
  "api_keys": "test,abc123"
}

// Don't typo file paths
{
  "api_keys": "config/api_keyz.txt"
}

// Don't use directories
{
  "api_keys": "config/"
}
```

## Generating Secure Keys

```bash
# Generate a single strong key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate multiple keys
python -c "import secrets; print('\n'.join(secrets.token_urlsafe(32) for _ in range(5)))"
```

Output:

```text
Xk9mP2vN4wQ8rL6hJ5fD1sA7yU0bC3eK9nM3pR2t
yU0bC3eK9nM3pR2tXk9mP2vN4wQ8rL6hJ5fD1sA7
qW3eR5tY7uI9oP1aS2dF4gH6jK8lZ0xCvBnM3qW5
zX2cV4bN6mM8kL0jH3gF5dS7aP9oI1uY3tR6eW8q
pO9iU8yT7rE6wQ5aSdFgHjKlZxCvBnM1qW2eR3tY
```
