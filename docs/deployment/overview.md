# Deployment Overview

Deploy your Apiary API to production.

## Deployment Options

### 1. Traditional Server (Recommended)

- nginx as reverse proxy
- systemd for process management
- gunicorn with uvicorn workers

See [Server Setup](server-setup.md) for details.

### 2. Docker

Apiary includes a `Dockerfile` and `docker-compose.yml`. Config and services are
bind-mounted so you can edit them without rebuilding the image.

```bash
uv run apiary docker up --build
```

See [Docker Deployment](docker.md) for full details.

## Quick Deployment Checklist

- [ ] Install Python 3.12+ and dependencies
- [ ] Configure `config/settings.json` with production keys
- [ ] Set up nginx reverse proxy
- [ ] Configure systemd service
- [ ] Enable SSL/TLS (Let's Encrypt)
- [ ] Set up monitoring and logging
- [ ] Configure backups
- [ ] Test health endpoints

## Initial Deployment

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/lancereinsmith/apiary.git /path/to/apiary
cd /path/to/apiary

# Install dependencies
uv sync

# Initialize configuration and custom directories
uv run apiary init
# Creates config/settings.json, config/endpoints.json,
# services_custom/, and routers_custom/ (gitignored)
```

### 2. Configure for Production

Edit your configuration files with production values:

```bash
# Edit settings
nano config/settings.json

# Edit endpoints (if needed)
nano config/endpoints.json
```

!!! important "Configuration Files are Gitignored"
    The files `config/settings.json` and `config/endpoints.json` are automatically
    ignored by git (see `.gitignore`). This means your production configuration
    **will never be committed** and **won't cause merge conflicts** when you pull updates.

### 3. Start the Service

See [Server Setup](server-setup.md) for complete systemd/nginx setup.

## Updating Your Deployment

Apiary is designed for **update-safe deployment** with gitignored configuration files.

### Quick Update

```bash
cd /path/to/apiary
git pull origin main
uv sync
sudo systemctl restart apiary
```

Your configuration files are never touched by git operations.

### What You Need to Know

- **Configuration is preserved** - `config/settings.json`, `config/endpoints.json`, and key files are gitignored
- **Custom code is safe** - `services_custom/` and `routers_custom/` are never overwritten
- **Test before restarting** - Use `uv run apiary test` to validate updates
- **Backup first** - Run `uv run apiary backup --include-custom` before major updates
- **Easy rollback** - Use `git checkout <commit-hash>` if issues arise

See [Updating Your Deployment](updating.md) for comprehensive update workflows, rollback strategies, version pinning, and automation.

## Next Steps

- [Docker Deployment](docker.md) - Docker and docker-compose setup
- [Server Setup](server-setup.md) - Detailed server setup
- [Configuration](configuration.md) - Production configuration
- [Monitoring](monitoring.md) - Set up monitoring
