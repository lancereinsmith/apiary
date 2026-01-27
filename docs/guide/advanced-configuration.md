# Advanced Configuration

Learn advanced configuration techniques for Apiary including environment files, update-safe deployment patterns, and security best practices.

## Using Environment Files

Apiary automatically loads environment variables from a `.env` file if it exists in the project root.

Create a `.env` file:

```bash
# .env
API_KEYS=key1,key2,key3
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
```

Environment variables take precedence over `config/settings.json`.

!!! note
    The `.env` file is automatically loaded on application startup. No additional configuration needed!

### Environment Variable Names

All settings can be overridden with environment variables:

```bash
export API_KEYS="key1,key2"
export RATE_LIMIT_ENABLED=true
export RATE_LIMIT_PER_MINUTE=100
export RATE_LIMIT_PER_MINUTE_AUTHENTICATED=500

uv run apiary serve --reload
```

## Configuration Priority Order

Configuration is loaded in this order (higher numbers override lower):

1. Default values in code
2. `config/settings.json` file
3. Environment variables

This allows you to:

- Set sensible defaults in `settings.json`
- Override specific values with environment variables in prodiuction

## Configuration Inheritance

You can have multiple configuration files for different environments:

```bash
config/settings.json           # Base settings
config/settings.dev.json       # Development overrides
config/settings.prod.json      # Production overrides
```

Load different configs by specifying the file:

```python
from config import Settings
from pathlib import Path

# Load production config
settings = Settings.from_json_file(Path("config/settings.prod.json"))
```

## Programmatic Configuration

Override settings in code:

```python
from config import Settings

# Create custom settings
settings = Settings(
    api_keys="custom-key",
    rate_limit_enabled=True,
    rate_limit_per_minute=100
)
```

This is useful for:

- Testing with custom configurations
- Creating dynamic configurations
- Integrating with configuration management systems

## Update-Safe Configuration

Apiary's configuration system is designed to be **update-safe**, meaning you can deploy Apiary to your server, customize it, and still pull updates without conflicts.

### How It Works

1. **Templates are tracked** - `settings_template.json` and `endpoints_template.json` are in git
2. **Your config is gitignored** - `settings.json` and `endpoints.json` are not tracked
3. **Custom code lives in gitignored dirs** - `services_custom/` and `routers_custom/` (created by `apiary init`) are never overwritten by `git pull`
4. **Updates are safe** - Running `git pull` never touches your configuration or custom code

### Workflow

```bash
# Initial setup on server
git clone https://github.com/lancereinsmith/apiary.git
cd apiary
uv sync
uv run apiary init              # Creates config + services_custom/, routers_custom/

# Edit config/settings.json
# Put custom services in services_custom/, routers in routers_custom/

# Later, when updates are available
git pull origin main            # Your config is preserved!
uv sync                         # Update dependencies
uv run apiary test              # Verify update works
sudo systemctl restart apiary   # Restart with new code
```

### Checking for New Options

After pulling updates, check if new configuration options were added:

```bash
# See what changed in templates
git log --oneline -10 -- config/*_template.json

# Compare template with your config
diff config/settings_template.json config/settings.json

# If you see new options you want, manually add them to your config
nano config/settings.json
```

### Why This Matters

- Pull bug fixes and new features anytime
- Keep sensitive data (API keys) out of version control
- Maintain multiple deployments (dev, staging, prod) with different configs
- Preserve settings in `config/settings.json` and `config/endpoints.json` without overwritng
- Add custom services and routers in `services_custom/` and `routers_custom/` without merge conflicts

## Security Best Practices

### Protecting Sensitive Data

1. **Never commit** sensitive files to version control (already gitignored!)
2. **Use strong API keys** (32+ characters, random)
3. **Rotate keys regularly** in production
4. **Use environment variables** for CI/CD

### Generating Strong API Keys

Generate cryptographically secure API keys:

```bash
# Generate a single key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate multiple keys
python -c "import secrets; print('\n'.join(secrets.token_urlsafe(32) for _ in range(3)))"
```

Example output:

```text
7xK9mP4nQ2wR8vL5hT6jY3zN1sF0dG4bC8aM7eX2qW9uI5oP3tA1yH6kL
2pQ8wR5tY9uI4oP7aS3dF6gH1jK0lZ4xC7vB2nM5qW8eR3tY6uI9oP1aS
5dF8gH2jK6lZ9xC4vB7nM1qW3eR5tY8uI0oP2aS4dF7gH9jK3lZ6xC1vB
```

### API Key Management

**Option 1: Inline keys** (for development):

```json
{
  "api_keys": "client1-key,client2-key,admin-key"
}
```

**Option 2: Key files** (recommended for production):

```json
{
  "api_keys": "config/api_keys.txt"
}
```

Key file format (one key per line, supports comments):

```text
# config/api_keys.txt
# Production API keys - rotate quarterly

# Client 1 - issued 2024-01-15
client1-7xK9mP4nQ2wR8vL5hT6jY3zN1sF0dG4b

# Client 2 - issued 2024-01-20
client2-2pQ8wR5tY9uI4oP7aS3dF6gH1jK0lZ4x

# Admin key - issued 2024-02-01
admin-5dF8gH2jK6lZ9xC4vB7nM1qW3eR5tY8u
```

**Benefits of key files**:

- One key per line (readable)
- Comments for documentation
- Automatic hot-reloading (no restart needed)
- Easy key rotation

### Rate Limiting Configuration

Configure rate limits to protect your API:

```json
{
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,                    // Public: 60 req/min
  "rate_limit_per_minute_authenticated": 300      // Authenticated: 300 req/min
}
```

**Recommendations**:

- **Public endpoints**: 60-120 requests/minute (prevent abuse)
- **Authenticated**: 300-1000 requests/minute (trusted clients)
- **Disable for development**: Set `rate_limit_enabled: false` locally

### File Permissions

Restrict access to configuration files:

```bash
# Make config files readable only by owner
chmod 600 config/settings.json
chmod 600 config/endpoints.json
chmod 600 config/api_keys.txt

# Verify permissions
ls -la config/
```

Expected output:

```text
-rw------- 1 user user  245 Jan 26 10:00 settings.json
-rw------- 1 user user  123 Jan 26 10:00 endpoints.json
-rw------- 1 user user   89 Jan 26 10:00 api_keys.txt
```

### Production Security Checklist

- [ ] Strong API keys (32+ characters)
- [ ] Keys stored in separate files (not inline)
- [ ] File permissions set to 600
- [ ] `.env` and `config/*.json` in `.gitignore`
- [ ] Rate limiting enabled
- [ ] HTTPS/TLS configured (via nginx)
- [ ] Regular key rotation schedule
- [ ] Monitoring and alerting enabled

## Per-Endpoint Configuration

Advanced endpoint configurations including authentication, rate limiting, and parameter validation.

### Endpoint-Specific API Keys

Override global API keys for specific endpoints:

```json
{
  "path": "/api/admin",
  "method": "POST",
  "service": "admin",
  "enabled": true,
  "requires_auth": true,
  "api_keys": "config/admin_keys.txt",
  "description": "Admin endpoint (requires special key)"
}
```

This allows:

- Different keys for different endpoints
- Separate admin/client keys
- Fine-grained access control

### Custom Rate Limits

Set custom rate limits per endpoint:

```json
{
  "path": "/api/expensive-operation",
  "method": "POST",
  "service": "expensive",
  "enabled": true,
  "requires_auth": true,
  "rate_limit_per_minute": 10,
  "description": "Resource-intensive operation (limited to 10/min)"
}
```

### Complex Parameter Mapping

Advanced parameter configurations:

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
      "key": "limit",
      "default": 10
    },
    "api_version": "v1"
  }
}
```

Parameter sources:

- **`path`** - Extract from URL path (e.g., `/api/user/{id}`)
- **`query`** - Extract from query string (e.g., `?q=search`)
- **`body`** - Extract from request body (POST/PUT)
- **Static value** - Use a hardcoded string (e.g., `"api_version": "v1"`)

## Configuration Validation

### Validating Configuration Files

Use the CLI to validate your configuration:

```bash
# Validate configuration
uv run apiary validate-config

# Test full application (config + imports)
uv run apiary test
```

### Common Validation Errors

**Invalid JSON syntax**:

```text
ERROR: Failed to parse config/settings.json: Expecting ',' delimiter: line 5 column 3
```

**Fix**: Check for missing commas, quotes, or brackets.

**Missing service**:

```text
WARNING: Service 'unknown_service' referenced in endpoint but not registered
```

**Fix**: Ensure service is defined in `services/` or `services_custom/`.

**Invalid endpoint path**:

```text
ERROR: Endpoint path 'api/test' must start with '/'
```

**Fix**: Change to `/api/test`.

**Weak API key**:

```text
WARNING: API key 'test123' is very short (7 chars). Use 32+ chars for production.
```

**Fix**: Generate a strong key with `python -c "import secrets; print(secrets.token_urlsafe(32))"`.

## Configuration Reference

For complete details on all configuration options, see:

- [Configuration Options Reference](../reference/config.md)
- [Basic Configuration](../getting-started/configuration.md)
- [Deployment Configuration](../deployment/configuration.md)

## Next Steps

- [API Key Validation](api-key-validation.md) - Detailed validation guide
- [Authentication](authentication.md) - Implement auth patterns
- [Creating Services](creating-services.md) - Build custom services
- [Deployment Configuration](../deployment/configuration.md) - Production settings
