# Deployment Configuration

Configure Apiary for production deployment.

## Production Settings

```json
{
  "api_keys": "strong-random-key-1,strong-random-key-2",
  "enable_landing_page": true,
  "rate_limit_enabled": true,
  "rate_limit_per_minute": 60,
  "rate_limit_per_minute_authenticated": 300
}
```

## Environment Variables

```bash
export API_KEYS="prod-key-1,prod-key-2"
export RATE_LIMIT_ENABLED=true
```

## Security

1. **Use strong API keys** (32+ characters)
2. **Enable HTTPS** with SSL/TLS
3. **Restrict file permissions**: `chmod 600 settings.json`
4. **Use environment variables** for secrets
5. **Enable rate limiting**

## Performance Tuning

### Gunicorn Workers

```bash
# In systemd service file
ExecStart=gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:api
```

Workers = (2 × CPU cores) + 1

### nginx

```nginx
worker_processes auto;
worker_connections 1024;
```

## Next Steps

- [Monitoring](monitoring.md) - Set up monitoring
- [Server Setup](server-setup.md) - Initial setup

