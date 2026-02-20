# Server Setup

Deploy Apiary to a server with nginx and systemd.

## Prerequisites

- Ubuntu 20.04+ or Debian 11+ server (e.g. AWS Lightsail)
- Python 3.12+
- nginx
- systemd

---

## Automated Install (Recommended)

The `_server/scripts/install.sh` script handles the full setup in one pass:
packages, uv, git clone, dependencies, config init, nginx, and systemd.

```bash
# Clone the repo first, then run the installer
git clone https://github.com/lancereinsmith/apiary.git
bash apiary/_server/scripts/install.sh --domain api.example.com
```

`--domain` is optional — the script will prompt for it if omitted.

What it does:

1. Installs `git`, `nginx`, `curl`, and `certbot` via `apt`
2. Installs `uv` (if not already present)
3. Clones the repository to `~/apiary`
4. Runs `uv sync --frozen --no-dev` (production dependencies only)
5. Creates the `logs/` directory
6. Runs `apiary init` to generate config files (skipped if they already exist)
7. Generates a random 256-bit `SECRET_KEY` and injects it into the systemd service
8. Adds your user to the `www-data` group for unix socket access
9. Copies and patches the nginx config with your domain
10. Copies and enables the systemd service

After the script finishes:

```bash
# Edit config with your API keys and settings
nano ~/apiary/config/settings.json

# Start the service
sudo systemctl start apiary
sudo systemctl status apiary

# Optional: enable HTTPS
sudo certbot --nginx -d api.example.com
```

---

## Manual Installation

Follow these steps if you prefer to set things up by hand.

### 1. Install Dependencies

```bash
sudo apt update
sudo apt install git nginx curl python3-certbot-nginx

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup

```bash
cd ~
git clone https://github.com/lancereinsmith/apiary.git
cd apiary

uv sync --frozen --no-dev

# Initialize configuration
uv run apiary init

# Edit with production values
nano config/settings.json
```

### 3. Configure nginx

```bash
sudo cp _server/nginx/apiary.nginx /etc/nginx/sites-available/apiary

# Update server_name to your domain
sudo nano /etc/nginx/sites-available/apiary

sudo ln -s /etc/nginx/sites-available/apiary /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Configure systemd

```bash
sudo cp _server/systemd/apiary.service /etc/systemd/system/apiary.service

# Set your SECRET_KEY
sudo nano /etc/systemd/system/apiary.service

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable apiary
sudo systemctl start apiary
sudo systemctl status apiary
```

### 5. SSL/TLS (Recommended)

```bash
sudo certbot --nginx -d yourdomain.com
```

---

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
