# Changelog

All notable changes to Apiary will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-02-21

### Added

- **Docker Compose support**: `docker-compose.yml` runs the application on host port 3002
  with `config/` and `services/` bind-mounted as volumes for live editing without rebuilds
- **Config validation at container startup**: Dockerfile CMD now runs `apiary test` before
  launching uvicorn — the container exits immediately if `settings.json` or `endpoints.json`
  are invalid
- **`apiary docker` CLI commands**: New subcommand group for managing the Docker container:
  - `apiary docker up [--build]` — start the container in the background; `--build` rebuilds the image first
  - `apiary docker down` — stop and remove the container
  - `apiary docker restart` — restart the container (use after editing mounted volumes)
- **Docker deployment docs**: `docs/deployment/docker.md` covers volumes, startup validation,
  and the typical edit→restart workflow

---

## [0.2.0] - 2026-02-20

### Added

- **AWS Lightsail install script**: `_server/scripts/install.sh` automates full server setup — installs system packages (`git`, `nginx`, `curl`, `certbot`), installs `uv`, clones the repository, syncs production dependencies, initializes config, generates a random 256-bit `SECRET_KEY`, configures nginx and systemd, and enables the service
- **Update script**: `_server/scripts/update.sh` provides a one-command update workflow (`git pull` → `uv sync` → `systemctl restart`)
- **Deployment docs**: Updated `server-setup.md` to lead with the automated install script; updated `updating.md` to document `update.sh` as the recommended update path

### Fixed

- **systemd service**: Changed `Group=nginx` to `Group=www-data` — on Ubuntu/Debian, nginx runs as `www-data`, not `nginx` (which is an RHEL/CentOS convention)

---

## [0.1.1] - 2026-02-14

### Fixed

- **pytest-asyncio version**: Changed from `>=1.3.0` (nonexistent) to `>=0.24.0`
- **pytest.ini**: Removed buggy `--ignore=tests` directive that contradicted `testpaths=tests`, consolidated all pytest config into `pyproject.toml`
- **HTTPMethod enum**: Migrated from `(str, Enum)` to `StrEnum` (Python 3.12+, fixes ruff UP042)

### Changed

- **Health readiness probe**: Removed hardcoded CoinLore crypto API dependency check from `/health/ready`; now checks configuration validity and reports registered services without coupling to specific service implementations
- **CLI serve command**: Changed `host` and `port` from positional arguments to `--host`/`-h` and `--port`/`-p` options with defaults shown
- **Service registry exports**: Added `__all__` to `core/services/__init__.py` for clean public API

### Added

- **`py.typed` marker**: PEP 561 compliance for downstream type checking
- **Multi-worker documentation**: Added warnings to `RateLimiter` and `MetricsCollector` classes noting that in-memory state is per-process and not shared across Gunicorn workers
- **Deployment docs**: Added multi-worker caveats to monitoring and deployment configuration guides
- **Version bump**: `0.1.0` to `0.1.1` in `pyproject.toml`

---

## [0.1.0] - 2026-01-26

### Added

#### Core Framework

- FastAPI-based modular API framework
- Dynamic endpoint creation from JSON configuration
- Service-based architecture with `BaseService` class
- Dependency injection for services and settings
- Structured logging with correlation IDs and request tracking
- Custom exception handling with detailed error responses

#### Authentication & Security

- API key authentication system with header-based validation
- Support for inline API keys (comma-separated strings)
- File-based API key management with automatic reloading
- Endpoint-specific API key configuration (override global keys)
- Optional authentication for public endpoints
- API key validation CLI tool

#### Rate Limiting

- Configurable rate limiting per minute
- Separate limits for authenticated and unauthenticated requests
- IP-based rate tracking

#### Built-in Endpoints

- `GET /` - HTML landing page with API information
- `GET /health` - Basic health check
- `GET /health/live` - Kubernetes liveness probe
- `GET /health/ready` - Kubernetes readiness probe with dependency checks
- `GET /metrics` - Application metrics (requests, errors, uptime)
- `GET /endpoints` - Endpoint discovery (lists all registered endpoints)
- `GET /auth/status` - Check authentication status
- `POST /auth/validate` - Validate API key

#### Services

- `HelloService` - Simple greeting service (example/demo)
- `CryptoService` - Cryptocurrency price data from CoinCap API

#### Configuration

- JSON-based configuration files (`settings.json`, `endpoints.json`)
- Template files for easy initialization
- Pydantic-based settings validation
- Environment variable support
- Configurable API documentation (Swagger UI, ReDoc, OpenAPI JSON)
- Router enable/disable configuration

#### CLI Tools

- `apiary init` - Initialize configuration from templates
- `apiary serve` - Start the development server with optional reload
- `apiary validate-config` - Validate API key configurations
- `apiary clean` - Clean up generated files and caches

#### Documentation

- Complete user guide with examples
- Getting started guide (installation, quickstart, configuration)
- Advanced topics (authentication, API key validation, advanced endpoints)
- Deployment guides (server setup, configuration, monitoring)
- API reference (core modules, services, models, configuration)
- CLI reference with detailed command documentation

#### Deployment

- nginx reverse proxy configuration template
- systemd service unit template
- Docker support
- Production configuration examples
- Health check endpoints for orchestration

### Technical Details

- Python 3.12+ required
- Built with FastAPI 0.128.0+
- Uses Pydantic v2 for data validation
- Uvicorn ASGI server with uvloop
- Watchdog for file monitoring
- httpx for async HTTP requests

---

## Release Notes

### Version Compatibility

- **Python**: 3.12 or higher required
- **FastAPI**: 0.128.0 or higher
- **Pydantic**: 2.5.0 or higher

### Upgrade Notes

#### From 0.2.0 to 0.3.0

- No API or configuration changes — this release adds Docker Compose support and CLI docker commands.
- If you already have a `docker-compose.yml`, replace it with the new one (port 3002, mounted volumes).
- The Dockerfile CMD now runs `apiary test` on startup; ensure `config/settings.json` and
  `config/endpoints.json` exist and are valid before starting the container.

#### From 0.1.1 to 0.2.0

- **systemd service**: If you have an existing deployment, update the `Group=` in your service file: `sudo sed -i 's/Group=nginx/Group=www-data/' /etc/systemd/system/apiary.service && sudo systemctl daemon-reload && sudo systemctl restart apiary`
- No API or configuration changes — this release is purely infrastructure and tooling.

#### From 0.1.0 to 0.1.1

- **CLI**: `apiary serve HOST PORT` is now `apiary serve --host HOST --port PORT`. The old positional syntax no longer works.
- **Health check**: `/health/ready` no longer checks the CoinLore API. If you were relying on the `crypto_api` field in the readiness response, it has been replaced by a `services` field listing all registered services.
- **pytest config**: `pytest.ini` has been removed. All pytest configuration is now in `pyproject.toml`. If you had local customizations in `pytest.ini`, migrate them to `[tool.pytest.ini_options]` in `pyproject.toml`.

### Breaking Changes

- `apiary serve` positional arguments replaced with `--host`/`--port` options (v0.1.1)

---

[0.1.0]: https://github.com/lancereinsmith/apiary/releases/tag/v0.1.0
[0.1.1]: https://github.com/lancereinsmith/apiary/releases/tag/v0.1.1
[0.2.0]: https://github.com/lancereinsmith/apiary/releases/tag/v0.2.0
[0.3.0]: https://github.com/lancereinsmith/apiary/releases/tag/v0.3.0
[Unreleased]: https://github.com/lancereinsmith/apiary/compare/v0.3.0...HEAD
