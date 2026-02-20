#!/usr/bin/env bash
# update.sh — Pull the latest code and restart Apiary.
#
# Usage:
#   bash update.sh
#
# Run as the `ubuntu` user from any directory.

set -euo pipefail

APP_DIR="$HOME/apiary"
SERVICE_NAME="apiary"

info() { echo "  [+] $*"; }
step() { echo; echo "── $* ──────────────────────────────────────────────"; }

# ── Pull latest code ───────────────────────────────────────────────────────
step "Git pull"
cd "$APP_DIR"
git pull --ff-only
info "Repository updated"

# ── Sync dependencies ──────────────────────────────────────────────────────
step "Dependencies"
uv sync --frozen --no-dev
info "Dependencies synced"

# ── Restart service ────────────────────────────────────────────────────────
step "Service restart"
sudo systemctl restart "$SERVICE_NAME"
sudo systemctl status "$SERVICE_NAME" --no-pager
info "Apiary restarted"

echo
echo "  Update complete. Check logs with: sudo journalctl -u apiary -f"
echo
