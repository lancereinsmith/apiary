# Installation

Get Apiary up and running on your system.

## Prerequisites

- **Python 3.11+** installed
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
cp settings_template.json settings.json
cp config/endpoints_template.json config/endpoints.json

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

### As a Template

Use Apiary as a GitHub template:

1. Visit the [Apiary repository](https://github.com/lancereinsmith/apiary)
2. Click "Use this template"
3. Create your new repository
4. Clone and set up:

```bash
git clone https://github.com/yourusername/your-api.git
cd your-api
uv sync
cp settings_template.json settings.json
```

## Configuration

### 1. Settings

Edit `settings.json`:

```json
{
  "api_keys": "your-secret-key-here",
  "enable_landing_page": true,
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
      "description": "Get cryptocurrency data"
    }
  ]
}
```

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
cp settings_template.json settings.json
```

### Import Errors

```bash
# Reinstall dependencies
uv sync --reinstall
```

## Development Dependencies

For development work:

```bash
uv sync --group dev
```

This installs:
- pytest, pytest-asyncio, pytest-cov (testing)
- black (formatting)
- ruff (linting)
- mypy (type checking)

## What's Installed

Core dependencies:

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **Jinja2** - Template engine

Production features:

- Rate limiting
- Metrics collection
- Health checks
- Authentication
- Request validation
- Structured logging

## Next Steps

1. [Quick Start](quickstart.md) - Build your first endpoint
2. [Configuration Guide](configuration.md) - Learn configuration options
3. [Adding Endpoints](../guide/adding-endpoints.md) - Create endpoints
