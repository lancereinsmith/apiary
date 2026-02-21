# CLI Reference

Apiary includes a comprehensive command-line interface (CLI) for common maintenance and development tasks. All commands are accessed through a single `apiary` entry point with various subcommands.

## Overview

The CLI is built with [Click](https://click.palletsprojects.com/) and provides a consistent interface for:

- Starting the development server
- Initializing and validating configuration
- Backing up configuration and custom code
- Testing application before deployment
- Cleaning up generated files
- Managing the Docker container (`docker up`, `docker down`, `docker restart`)

## Installation

The CLI is automatically installed when you install Apiary:

```bash
uv sync
```

## Usage

All commands follow this pattern:

```bash
uv run apiary [OPTIONS] COMMAND [ARGS]...
```

### Getting Help

```bash
# Show all available commands
uv run apiary --help

# Show help for a specific command
uv run apiary serve --help
uv run apiary init --help

# Show version
uv run apiary --version
```

## Commands

::: mkdocs-click
    :module: cli
    :command: cli
    :prog_name: apiary
    :depth: 1

## Exit Codes

All commands return standard exit codes:

- `0` - Success
- Non-zero - Failure

This makes them suitable for use in scripts and CI/CD pipelines.

## Output Formatting

The CLI uses colored output for better readability:

- 🔧 Blue - Command running
- ✅ Green - Success
- ❌ Red - Failure
- 📊 - Informational messages

---

## Next Steps

- [Configuration Guide](../getting-started/configuration.md)
- [Adding Endpoints](../guide/adding-endpoints.md)
- [API Key Validation Guide](../guide/api-key-validation.md)
