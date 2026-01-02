# CLI Reference

Apiary includes a comprehensive command-line interface (CLI) for common maintenance and development tasks. All commands are accessed through a single `apiary` entry point with various subcommands.

## Overview

The CLI is built with [Click](https://click.palletsprojects.com/) and provides a consistent interface for:

- Running tests and generating coverage reports
- Code formatting and linting
- Type checking
- Building and deploying documentation
- Starting the development server
- Cleaning up generated files

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
uv run apiary test --help
uv run apiary docs-serve --help

# Show version
uv run apiary --version
```

## Commands

### Testing

#### `test`

Run the test suite using pytest.

**Usage:**

```bash
uv run apiary test [OPTIONS]
```

**Options:**

- `-v, --verbose` - Enable verbose output
- `-c, --coverage` - Run tests with coverage report

**Examples:**

```bash
# Run all tests
uv run apiary test

# Run with verbose output
uv run apiary test -v

# Run with coverage
uv run apiary test --coverage
```

#### `coverage`

Generate a detailed coverage report with optional HTML output.

**Usage:**

```bash
uv run apiary coverage [OPTIONS]
```

**Options:**

- `--html` - Generate HTML coverage report (default: true)
- `-o, --open-browser` - Open the HTML report in browser after generation

**Examples:**

```bash
# Generate coverage report
uv run apiary coverage

# Generate and open in browser
uv run apiary coverage -o
```

The HTML report is generated in `htmlcov/index.html`.

---

### Code Quality

#### `format-code`

Format Python code using Black.

**Usage:**

```bash
uv run apiary format-code [OPTIONS]
```

**Options:**

- `--check` - Check formatting without modifying files

**Examples:**

```bash
# Format all Python files
uv run apiary format-code

# Check formatting without changes
uv run apiary format-code --check
```

#### `lint`

Run the Ruff linter to check for code quality issues.

**Usage:**

```bash
uv run apiary lint [OPTIONS]
```

**Options:**

- `--fix` - Automatically fix issues where possible

**Examples:**

```bash
# Check for linting issues
uv run apiary lint

# Fix issues automatically
uv run apiary lint --fix
```

#### `typecheck`

Run MyPy for static type checking.

**Usage:**

```bash
uv run apiary typecheck
```

**Example:**

```bash
uv run apiary typecheck
```

#### `check-all`

Run all code quality checks in sequence: formatting, linting, type checking, and tests.

**Usage:**

```bash
uv run apiary check-all [OPTIONS]
```

**Options:**

- `--fix` - Automatically fix issues where possible (for format and lint)

**Examples:**

```bash
# Run all checks
uv run apiary check-all

# Run all checks and auto-fix issues
uv run apiary check-all --fix
```

This command provides a summary at the end showing which checks passed or failed:

```
Summary:
===============================================================
Format          ✅ PASSED
Lint            ✅ PASSED
Type Check      ✅ PASSED
Tests           ✅ PASSED

🎉 All checks passed!
```

---

### Documentation

#### `docs-serve`

Serve documentation locally using MkDocs.

**Usage:**

```bash
uv run apiary docs-serve [OPTIONS]
```

**Options:**

- `-p, --port INTEGER` - Port to serve on (default: 8000)

**Examples:**

```bash
# Serve on default port (8000)
uv run apiary docs-serve

# Serve on custom port
uv run apiary docs-serve -p 8001
```

Visit `http://127.0.0.1:8000` (or your custom port) to view the documentation.

#### `docs-build`

Build the documentation site to the `site/` directory.

**Usage:**

```bash
uv run apiary docs-build
```

**Example:**

```bash
uv run apiary docs-build
```

The built documentation will be in the `site/` directory.

#### `docs-deploy`

Deploy documentation to GitHub Pages.

**Usage:**

```bash
uv run apiary docs-deploy [OPTIONS]
```

**Options:**

- `-m, --message TEXT` - Custom deployment commit message

**Examples:**

```bash
# Deploy with default message
uv run apiary docs-deploy

# Deploy with custom message
uv run apiary docs-deploy -m "Update API reference"
```

This command:

1. Builds the documentation
2. Pushes it to the `gh-pages` branch
3. GitHub Pages automatically publishes it

---

### Server Management

#### `serve`

Start the Apiary API server.

**Usage:**

```bash
uv run apiary serve [HOST] [PORT] [OPTIONS]
```

**Arguments:**

- `HOST` - Host address (default: 127.0.0.1)
- `PORT` - Port number (default: 8000)

**Options:**

- `--reload` - Enable auto-reload for development

**Examples:**

```bash
# Start on default host/port
uv run apiary serve

# Start on custom host and port
uv run apiary serve 0.0.0.0 8080

# Start with auto-reload (development)
uv run apiary serve --reload
```

---

### Maintenance

#### `clean`

Remove generated files and caches to clean up your workspace.

**Usage:**

```bash
uv run apiary clean
```

**What it removes:**

- `__pycache__` directories
- `.pyc` and `.pyo` files
- `.pytest_cache`
- `.mypy_cache`
- `.ruff_cache`
- `htmlcov` (coverage reports)
- `.coverage` files
- `site` (built documentation)
- `*.egg-info` directories

**Example:**

```bash
uv run apiary clean
```

---

## Common Workflows

### Before Committing

Run all checks to ensure your changes are ready:

```bash
uv run apiary check-all --fix
```

### Development Loop

While developing, use auto-reload:

```bash
uv run apiary serve --reload
```

### Documentation Updates

1. Make changes to markdown files in `docs/`
2. Preview locally:

   ```bash
   uv run apiary docs-serve
   ```

3. Deploy when ready:

   ```bash
   uv run apiary docs-deploy
   ```

### Testing with Coverage

```bash
# Run tests with coverage
uv run apiary coverage

# Open the HTML report
uv run apiary coverage -o
```

### Continuous Integration

For CI pipelines, run all checks without auto-fixing:

```bash
uv run apiary check-all
```

---

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

## Extending the CLI

To add new commands, edit `cli.py` and add a new Click command:

```python
@cli.command()
@click.option('--option', help='An option')
def my_command(option):
    """My custom command."""
    run_command(['my-tool', '--flag'], 'Running my tool')
```

Then rebuild the package:

```bash
uv sync
```

Your new command will be available as:

```bash
uv run apiary my-command
```
