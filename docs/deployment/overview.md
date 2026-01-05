# Deployment Overview

Deploy your Apiary API to production.

## Deployment Options

### 1. Traditional Server (Recommended)

- nginx as reverse proxy
- systemd for process management
- gunicorn with uvicorn workers

See [Server Setup](server-setup.md) for details.

### 2. Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install uv && uv sync

CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Cloud Platforms

- AWS EC2
- Google Cloud Run
- Azure App Service
- DigitalOcean Droplets

## Quick Deployment Checklist

- [ ] Install Python 3.11+ and dependencies
- [ ] Configure `settings.json` with production keys
- [ ] Set up nginx reverse proxy
- [ ] Configure systemd service
- [ ] Enable SSL/TLS (Let's Encrypt)
- [ ] Set up monitoring and logging
- [ ] Configure backups
- [ ] Test health endpoints

## Next Steps

- [Server Setup](server-setup.md) - Detailed server setup
- [Configuration](configuration.md) - Production configuration
- [Monitoring](monitoring.md) - Set up monitoring

