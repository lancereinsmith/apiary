# Deployment Configuration

Configure Apiary for production deployment.

## Production Settings

### Using Inline Keys

```json
{
  "api_keys": "strong-random-key-1,strong-random-key-2",
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

### Using File-Based Keys (Recommended for Production)

```json
{
  "api_keys": "config/api_keys.txt",
  "enable_landing_page": true,
  "enable_docs": false,
  "enable_redoc": false,
  "enable_openapi": false,
  "enabled_routers": ["health", "metrics", "auth", "endpoints"],
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,
  "rate_limit_per_minute_authenticated": 300
}
```

Create `config/api_keys.txt`:

```text
# Production API keys
prod-key-xxxxxxxxxxxxxxxxx
prod-key-yyyyyyyyyyyyyyyyy
```

## Environment Variables

```bash
export API_KEYS="prod-key-1,prod-key-2"
export RATE_LIMIT_ENABLED=true
export ENABLE_DOCS=false
export ENABLE_REDOC=false
```

## Security

1. **Use strong API keys** (32+ characters, random)
2. **Use file-based keys** in production for easier rotation
3. **Enable HTTPS** with SSL/TLS
4. **Restrict file permissions**:
   ```bash
   chmod 600 config/settings.json
   chmod 600 config/api_keys.txt  # If using file-based keys
   ```
5. **Disable API docs in production** (`enable_docs`, `enable_redoc`, `enable_openapi`)
6. **Enable rate limiting**
7. **Use environment variables** for sensitive configuration

## Performance Tuning

### Gunicorn Workers

```bash
# In systemd service file
ExecStart=gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:api
```

Workers = (2 x CPU cores) + 1

!!! note "Multi-Worker Consideration"
    Rate limiting and metrics use in-memory storage that is not shared between
    workers. With 4 workers, clients effectively get 4x the configured rate
    limit and `/metrics` shows per-worker data. Use a single worker if accurate
    rate limiting is critical, or use Redis for shared state.

### nginx

```nginx
worker_processes auto;
worker_connections 1024;
```

## Next Steps

- [Server Setup](server-setup.md) - Initial setup
- [Updating](updating.md) - Update workflow and strategies
- [Monitoring](monitoring.md) - Set up monitoring
