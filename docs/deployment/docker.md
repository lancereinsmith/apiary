# Docker Deployment

Apiary ships with a `Dockerfile` and `docker-compose.yml` for running the application in
a container. The `config/` and `services/` directories are mounted as volumes so you can
edit them on the host without rebuilding the image.

## Quick Start

```bash
# Build the image and start the container
uv run apiary docker up --build

# Verify it is running
docker compose ps
```

The application is exposed on **host port 3002** and maps to container port 8000.

## CLI Commands

All Docker operations are available through the `apiary docker` subcommand group.

### `apiary docker up`

Start the container in the background.

```bash
# Start (image must already be built)
uv run apiary docker up

# Rebuild the image first, then start
uv run apiary docker up --build
```

Pass `--build` any time you change code that lives **outside** the mounted volumes (e.g.
core modules, `app.py`, `pyproject.toml`). Changes to `config/` and `services/` do not
require a rebuild — just a restart.

### `apiary docker down`

Stop and remove the container.

```bash
uv run apiary docker down
```

### `apiary docker restart`

Restart the running container. Use this after editing files inside the mounted `config/`
or `services/` volumes to make the application reload them.

```bash
uv run apiary docker restart
```

## Config Validation at Startup

The container entrypoint runs `apiary validate-config` before launching the server. If
`config/settings.json` or `config/endpoints.json` contain errors the container will exit
immediately with a non-zero code rather than starting a broken server.

```text
apiary validate-config   ← runs first; exits on failure
uvicorn ...   ← only starts if test passes
```

This means a misconfigured file surfaces as a container start failure, which is visible
in `docker compose logs` and prevents silently serving bad configuration.

## Volumes

| Host path  | Container path  | Purpose                                      |
|------------|-----------------|----------------------------------------------|
| `./config` | `/app/config`   | Settings, endpoints, and API key files        |
| `./services` | `/app/services` | Built-in and custom service modules         |

Changes to these directories take effect after a `docker compose restart` — no image
rebuild is needed.

## Typical Workflow

### After editing an endpoint or service

```bash
# 1. Edit config/endpoints.json and/or services/<your_service>.py on the host

# 2. Restart the container to reload changes
uv run apiary docker restart

# 3. Check logs to confirm clean startup
docker compose logs -f
```

### After changing core application code

```bash
# Rebuild the image (picks up changes outside mounted volumes)
uv run apiary docker up --build
```

### Stopping the service

```bash
uv run apiary docker down
```

## Logs

```bash
# Stream live logs
docker compose logs -f

# Show last 50 lines
docker compose logs --tail 50
```

## Next Steps

- [Updating Your Deployment](updating.md) — pull updates and restart
- [Configuration](configuration.md) — production configuration options
- [CLI Reference](../reference/cli.md) — all CLI commands
