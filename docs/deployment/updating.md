# Updating Your Deployment

One of Apiary's key design principles is **update-safe deployment**. Your configuration
files are gitignored, so you can safely pull updates without conflicts.

## Update Workflow

```bash
# Navigate to your deployment directory
cd /path/to/apiary

# Pull the latest changes (your config is safe!)
git pull origin main

# Update dependencies if needed
uv sync

# Restart the service
sudo systemctl restart apiary
```

That's it! Your local configuration files (`config/settings.json`, `config/endpoints.json`,
and any API key files) are preserved and never touched by git operations.

## What Gets Updated

When you run `git pull`, these files are updated:

- Core application code (`app.py`, `core/`, etc.)
- Routers and built-in endpoints (`routers/`)
- Base services (`services/`)
- Documentation (`docs/`)
- Template files (`config/*_template.json`)
- Dependencies (`pyproject.toml`, `requirements.txt`)

## What Stays Unchanged

These files and directories are gitignored and remain untouched:

- `config/settings.json` - Your API settings
- `config/endpoints.json` - Your endpoint configuration
- `config/api_keys.txt` - Your API key files
- `config/*_keys.txt` - Any other key files
- `.env` - Environment variables
- `services_custom/` - Your custom services
- `routers_custom/` - Your custom routers

## Custom Services and Routers

Put **custom services** in `services_custom/` and **custom routers** in `routers_custom/`.
These directories are gitignored, so your code is never overwritten by `git pull`.

```bash
# init creates these if they don't exist
uv run apiary init

# Your custom service (services_custom/weather_service.py)
# Your custom router (routers_custom/dashboard.py)
# Add "dashboard" to enabled_routers in config/settings.json
```

- **Services**: Same interface as built-in services; inherit from `BaseService`. They are
  discovered after `services/`, so a custom service with the same name overrides a built-in.
- **Routers**: Same as built-in; each module must define a `router` (APIRouter). Add the
  router name to `enabled_routers` in `config/settings.json`.

Do **not** put custom code in `services/` or `routers/`; those are updated by upstream
and can cause merge conflicts.

## Checking for New Template Options

After pulling updates, compare template files to see if new configuration options were added:

```bash
# Compare settings template with your config
diff config/settings_template.json config/settings.json

# Compare endpoints template with your config
diff config/endpoints_template.json config/endpoints.json
```

If you see new options in the template files that you want to use, manually add them
to your production configuration files.

## Testing Updates

Before restarting your production service, test the update:

```bash
# Run comprehensive tests (validates config and tests imports)
uv run apiary test

# Or test step-by-step:
# Validate configuration only
uv run apiary validate-config

# Test without importing the app (config only)
uv run apiary test --skip-import

# Start in test mode (if you have a separate test environment)
uv run apiary serve 127.0.0.1 8001
```

The `test` command validates your configuration and ensures the application can be
imported and initialized successfully, catching errors before you restart production.

## Rollback Strategy

If an update causes issues, you can easily roll back:

```bash
# View recent commits
git log --oneline -10

# Roll back to a specific commit
git checkout <commit-hash>

# Update dependencies to match that version
uv sync

# Restart service
sudo systemctl restart apiary
```

## Handling Breaking Changes

If a major update includes breaking changes, they will be documented in:

- `CHANGELOG.md` - Version history and breaking changes
- GitHub releases - Detailed release notes
- Documentation updates - Migration guides

Always check these resources before updating production deployments.

## Automatic Updates (Advanced)

For automated updates, create a script:

```bash
#!/bin/bash
# update-apiary.sh - Automated update script

set -e

cd /path/to/apiary

# Pull latest changes
git pull origin main

# Update dependencies
uv sync

# Test the update (validates config and tests imports)
uv run apiary test

# Restart service
sudo systemctl restart apiary

# Check if service is running
sleep 2
sudo systemctl is-active --quiet apiary && echo "✓ Service updated successfully" || echo "✗ Service failed to start"
```

## Version Pinning

For production stability, consider pinning to specific versions:

```bash
# Pin to a specific release tag
git fetch --tags
git checkout v1.2.3
uv sync
```

## Branching Strategy

Create a production branch for more control:

```bash
# Create production branch
git checkout -b production
git push origin production

# Update production branch when ready
git checkout production
git merge main
git push origin production

# On production server, pull from production branch
git pull origin production
```

## Configuration Backup

Always backup your configuration before updates:

```bash
# Backup configuration files
uv run apiary backup

# Backup configuration and custom code
uv run apiary backup --include-custom
```

This creates a timestamped backup in `backups/YYYYMMDD_HHMMSS/` with your configuration files. The backup directory is automatically excluded from git.

## Complete Update Workflow

Here's a comprehensive update workflow that includes all best practices:

```bash
# 1. Backup current configuration
uv run apiary backup --include-custom

# 2. Pull latest changes
git pull origin main

# 3. Update dependencies
uv sync

# 4. Test the update
uv run apiary test

# 5. Restart service
sudo systemctl restart apiary

# 6. Verify service is running
sudo systemctl status apiary

# 7. Check logs for errors
sudo journalctl -u apiary -n 50 --no-pager
```

## Next Steps

- [Server Setup](server-setup.md) - Detailed server setup
- [Configuration](configuration.md) - Production configuration
- [Monitoring](monitoring.md) - Set up monitoring
- [CLI Reference](../reference/cli.md) - All CLI commands
