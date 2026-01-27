# Installation

Get Apiary up and running on your system.

## Prerequisites

- **Python 3.12+** installed
- **[uv](https://github.com/astral-sh/uv)** package manager (recommended) or pip
- **Git** for cloning the repository

## Quick Install

```bash
# Clone the repository
git clone https://github.com/lancereinsmith/apiary.git
cd apiary

# Install dependencies
uv sync

# Create configuration
uv run apiary init

# Run the application
uv run apiary serve --reload
# Or using uvicorn directly
uvicorn app:api --reload
```

Visit `http://localhost:8000` to see your API running.

## Installation Methods

### Using uv (Recommended)

```bash
git clone https://github.com/lancereinsmith/apiary.git
cd apiary
uv sync
```

### Using pip

```bash
git clone https://github.com/lancereinsmith/apiary.git
cd apiary
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

### 1. Settings

Edit `config/settings.json`:

```json
{
  "api_keys": "your-api-key-1,your-api-key-2",
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

### 2. Endpoints (Optional)

Edit `config/endpoints.json` to configure dynamic endpoints:

```json
{
  "endpoints": [
    {
      "path": "/api/crypto",
      "method": "GET",
      "service": "crypto",
      "enabled": true,
      "requires_auth": false,
      "description": "Get cryptocurrency price data. Accepts optional 'symbol' parameter (e.g., BTC, ETH, SOL). Defaults to BTC if not provided.",
      "tags": ["crypto"],
      "summary": "Cryptocurrency price data"
    }
  ]
}
```

### 3. Environment Variables (Optional)

Apiary automatically loads environment variables from a `.env` file if present.

```bash
# Create .env file (optional)
# API_KEYS=your-secret-key
# RATE_LIMIT_ENABLED=true
```

!!! tip
    Environment variables override `config/settings.json` values. This is useful for keeping secrets out of version control.

## Verify Installation

### Run the Application

```bash
# Using CLI (recommended for development)
uv run apiary serve --reload

# Or using uvicorn directly
uvicorn app:api --reload
```

Expected output:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

### Run Tests

```bash
pytest              # All tests
pytest --cov        # With coverage
```

## Troubleshooting

### Port Already in Use

```bash
# Use different port
uvicorn app:api --port 8001
# Or use CLI
uv run apiary serve 127.0.0.1 8001
```

### Settings File Not Found

```bash
uv run apiary init
```

Or manually:

```bash
cp config/settings_template.json config/settings.json
cp config/endpoints_template.json config/endpoints.json
```

### Import Errors

```bash
# Reinstall dependencies
uv sync --reinstall
```

## What's Installed

Core dependencies:

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **Jinja2** - Template engine
- **python-dotenv** - Environment file loading

## Updating Apiary

Apiary is designed to be **update-safe**. Your configuration files are gitignored, so you can pull updates without conflicts:

```bash
# Pull latest updates
git pull origin main

# Update dependencies
uv sync

# Restart the server
# Your config files (settings.json, endpoints.json) are preserved!
```

This means you can:

- Deploy Apiary to your server
- Customize configuration for your needs
- Pull bug fixes and new features anytime

See the [Deployment Guide](../deployment/overview.md#updating-your-deployment) for more details on production update workflows.

## Next Steps

1. [Quick Start](quickstart.md) - Build your first endpoint
2. [Configuration Guide](configuration.md) - Learn configuration options
3. [Adding Endpoints](../guide/adding-endpoints.md) - Create endpoints
