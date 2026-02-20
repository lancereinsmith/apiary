#!/usr/bin/env bash
# install.sh — Fresh install of Apiary on an AWS Lightsail Ubuntu instance.
#
# Usage:
#   bash install.sh [--domain example.com] [--repo https://github.com/you/apiary.git]
#
# Run as the `ubuntu` user (default Lightsail user). The script calls sudo
# internally wherever root is needed.

set -euo pipefail

# ── Defaults ───────────────────────────────────────────────────────────────
REPO_URL="https://github.com/lancereinsmith/apiary.git"
APP_DIR="$HOME/apiary"
SERVICE_NAME="apiary"
NGINX_CONF="/etc/nginx/sites-available/apiary"
SYSTEMD_UNIT="/etc/systemd/system/apiary.service"

# ── Helpers ────────────────────────────────────────────────────────────────
info()  { echo "  [+] $*"; }
warn()  { echo "  [!] $*"; }
step()  { echo; echo "── $* ──────────────────────────────────────────────"; }

# ── Arg parsing ────────────────────────────────────────────────────────────
DOMAIN=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --domain) DOMAIN="$2"; shift 2 ;;
        --repo)   REPO_URL="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [[ -z "$DOMAIN" ]]; then
    read -rp "Enter the server domain or public IP (e.g. api.example.com): " DOMAIN
fi

echo
echo "╔══════════════════════════════════════════════════════════╗"
echo "║            Apiary — AWS Lightsail Installer              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo "  Domain  : $DOMAIN"
echo "  Repo    : $REPO_URL"
echo "  App dir : $APP_DIR"
echo

# ── System packages ────────────────────────────────────────────────────────
step "System packages"
sudo apt-get update -qq
sudo apt-get install -y -qq git nginx curl python3-certbot-nginx
info "git, nginx, curl, certbot installed"

# ── uv ─────────────────────────────────────────────────────────────────────
step "uv (Python package manager)"
if ! command -v uv &>/dev/null; then
    info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Make uv available for the rest of this script
    export PATH="$HOME/.local/bin:$PATH"
    info "uv installed at $(command -v uv)"
else
    info "uv already installed: $(uv --version)"
fi

# ── Clone repository ───────────────────────────────────────────────────────
step "Repository"
if [[ -d "$APP_DIR/.git" ]]; then
    warn "Repository already exists at $APP_DIR — skipping clone."
else
    info "Cloning $REPO_URL..."
    git clone "$REPO_URL" "$APP_DIR"
fi

# ── Python dependencies ────────────────────────────────────────────────────
step "Python dependencies"
cd "$APP_DIR"
uv sync --frozen --no-dev
info "Dependencies installed in $APP_DIR/.venv"

# ── Directories ────────────────────────────────────────────────────────────
step "Log directory"
mkdir -p "$APP_DIR/logs"
info "Created $APP_DIR/logs"

# ── Init config ────────────────────────────────────────────────────────────
step "Apiary configuration"
if [[ ! -f "$APP_DIR/config/settings.json" ]]; then
    info "Running 'apiary init'..."
    uv run apiary init
    info "Config created — edit $APP_DIR/config/settings.json with your settings."
else
    warn "Config already exists — skipping init."
fi

# ── Generate secret key for systemd service ────────────────────────────────
step "Secret key"
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
info "Generated a random 256-bit secret key"

# ── www-data group for socket access ───────────────────────────────────────
# On Ubuntu/Debian, nginx runs as www-data (not nginx as on RHEL/CentOS).
# gunicorn creates the unix socket with Group=www-data so nginx can read it.
step "www-data group"
if ! id -nG "$USER" | grep -qw www-data; then
    sudo usermod -aG www-data "$USER"
    info "Added $USER to the www-data group (re-login required for group to take effect)"
else
    info "$USER is already in the www-data group"
fi

# ── nginx config ───────────────────────────────────────────────────────────
step "nginx"
sudo cp "$APP_DIR/_server/nginx/apiary.nginx" "$NGINX_CONF"
sudo sed -i "s/server_name apiary;/server_name ${DOMAIN};/" "$NGINX_CONF"

if [[ ! -L /etc/nginx/sites-enabled/apiary ]]; then
    sudo ln -s "$NGINX_CONF" /etc/nginx/sites-enabled/apiary
fi

# Remove default site to avoid conflicts
if [[ -L /etc/nginx/sites-enabled/default ]]; then
    sudo rm /etc/nginx/sites-enabled/default
    info "Removed default nginx site"
fi

sudo nginx -t
sudo systemctl enable nginx
sudo systemctl reload nginx
info "nginx configured and reloaded"

# ── systemd service ────────────────────────────────────────────────────────
step "systemd service"
sudo cp "$APP_DIR/_server/systemd/apiary.service" "$SYSTEMD_UNIT"
sudo sed -i "s|SECRET_KEY=your_secret_key_here|SECRET_KEY=${SECRET_KEY}|" "$SYSTEMD_UNIT"
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
info "Service enabled — start with: sudo systemctl start apiary"

# ── Done ───────────────────────────────────────────────────────────────────
echo
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Installation complete!                                  ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Next steps:                                             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo
echo "  1. Edit your config:"
echo "     nano $APP_DIR/config/settings.json"
echo
echo "  2. Start the service:"
echo "     sudo systemctl start apiary"
echo "     sudo systemctl status apiary"
echo
echo "  3. (Optional) Enable HTTPS with Let's Encrypt:"
echo "     sudo certbot --nginx -d $DOMAIN"
echo
echo "  4. Verify:"
echo "     curl http://$DOMAIN/health"
echo
