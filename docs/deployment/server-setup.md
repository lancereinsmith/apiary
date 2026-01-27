# Server Setup

Deploy Apiary to a server with nginx and systemd.

## Prerequisites

- Ubuntu 20.04+ or Debian 11+ server
- Python 3.12+
- nginx
- systemd

## Installation Steps

### 1. Install Dependencies

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip nginx

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
cd ~
git clone https://github.com/lancereinsmith/apiary.git
cd apiary

uv sync

# Initialize configuration
uv run apiary init

# Edit with production values
nano config/settings.json
```

### 3. Configure nginx

Copy nginx configuration:

```bash
sudo cp _server/nginx/apiary.nginx /etc/nginx/sites-available/apiary
sudo ln -s /etc/nginx/sites-available/apiary /etc/nginx/sites-enabled/

# Edit and update paths and domains
sudo nano /etc/nginx/sites-available/apiary

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Configure systemd

```bash
sudo cp _server/systemd/apiary.service /etc/systemd/system/apiary.service

# Edit and update paths
sudo nano /etc/systemd/system/apiary.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable apiary
sudo systemctl start apiary
sudo systemctl status apiary
```

### 5. SSL/TLS (Recommended)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Verification

```bash
# Check service
sudo systemctl status apiary

# Check logs
sudo journalctl -u apiary -f

# Test endpoint
curl https://yourdomain.com/health
```

## Next Steps

- [Configuration](configuration.md) - Production settings
- [Updating](updating.md) - Update workflow and strategies
- [Monitoring](monitoring.md) - Set up monitoring
