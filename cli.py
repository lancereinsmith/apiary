"""CLI commands for Apiary maintenance tasks."""

import subprocess
import sys
from pathlib import Path

import click

from __version__ import __version__


def run_command(cmd: list[str], description: str, check: bool = True) -> int:
    """Run a command and return the exit code."""
    click.echo(f"🔧 {description}...")
    click.echo(f"   Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode == 0:
        click.secho(f"✅ {description} succeeded", fg="green")
    else:
        click.secho(f"❌ {description} failed", fg="red")
        if check:
            sys.exit(result.returncode)
    return result.returncode


@click.group()
@click.version_option(version=__version__, prog_name="Apiary")
def cli():
    """Apiary - Personal API service maintenance CLI."""
    pass


@cli.command()
@click.option("--host", "-h", default="127.0.0.1", show_default=True, help="Bind host")
@click.option(
    "--port", "-p", type=int, default=8000, show_default=True, help="Bind port"
)
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def serve(host: str, port: int, reload: bool):
    """Start the API server."""
    cmd = ["uvicorn", "app:api", f"--host={host}", f"--port={port}"]
    if reload:
        cmd.append("--reload")
    click.echo(f"🚀 Starting Apiary API server at http://{host}:{port}")
    run_command(cmd, "Starting server")


_CUSTOM_SERVICE_INIT = '''"""Custom services (gitignored).

Add your service modules here. This directory is never overwritten by git pull,
so your custom code is safe when you pull updates from upstream.

Create service files that inherit from core.services.base.BaseService.
See docs/guide/creating-services.md for the service interface.
'''

_CUSTOM_ROUTER_INIT = '''"""Custom routers (gitignored).

Add your router modules here. Each module must define a `router` (APIRouter).
Enable your router by adding its name to enabled_routers in config/settings.json.

This directory is never overwritten by git pull.
'''


@cli.command()
@click.option("--force", "-f", is_flag=True, help="Overwrite existing config files")
@click.option(
    "--custom-dirs/--no-custom-dirs",
    default=True,
    help="Create services_custom/ and routers_custom/ for update-safe custom code",
    show_default=True,
)
def init(force: bool, custom_dirs: bool):
    """Initialize configuration files and optional custom code directories.

    Creates config from templates and, by default, services_custom/ and
    routers_custom/. Custom directories are gitignored so your code is never
    overwritten when you pull updates. Put custom services and routers there.
    """
    import shutil

    click.echo("🐝 Initializing Apiary configuration...")

    # Define template -> target mappings
    config_files = [
        ("config/settings_template.json", "config/settings.json"),
        ("config/endpoints_template.json", "config/endpoints.json"),
    ]

    success_count = 0
    skip_count = 0
    error_count = 0

    for template_path, target_path in config_files:
        template = Path(template_path)
        target = Path(target_path)

        # Check if template exists
        if not template.exists():
            click.secho(f"❌ Template not found: {template_path}", fg="red")
            error_count += 1
            continue

        # Check if target already exists
        if target.exists() and not force:
            click.secho(f"⏭️  Skipping {target_path} (already exists)", fg="yellow")
            skip_count += 1
            continue

        # Copy the file
        try:
            shutil.copy2(template, target)
            click.secho(f"✅ Created {target_path}", fg="green")
            success_count += 1
        except Exception as e:
            click.secho(f"❌ Failed to create {target_path}: {e}", fg="red")
            error_count += 1

    # Create custom directories (gitignored) for update-safe custom code
    if custom_dirs:
        for dir_name, init_doc in [
            ("services_custom", _CUSTOM_SERVICE_INIT),
            ("routers_custom", _CUSTOM_ROUTER_INIT),
        ]:
            custom_dir = Path(dir_name)
            init_file = custom_dir / "__init__.py"
            if not custom_dir.is_dir():
                try:
                    custom_dir.mkdir(parents=True)
                    init_file.write_text(init_doc.strip() + "\n", encoding="utf-8")
                    click.secho(
                        f"✅ Created {dir_name}/ (for custom code, gitignored)",
                        fg="green",
                    )
                    success_count += 1
                except Exception as e:
                    click.secho(f"❌ Failed to create {dir_name}/: {e}", fg="red")
                    error_count += 1
            elif not init_file.exists():
                try:
                    init_file.write_text(init_doc.strip() + "\n", encoding="utf-8")
                    click.secho(f"✅ Created {dir_name}/__init__.py", fg="green")
                    success_count += 1
                except Exception as e:
                    click.secho(
                        f"❌ Failed to create {dir_name}/__init__.py: {e}", fg="red"
                    )
                    error_count += 1

    # Summary
    click.echo()
    if success_count > 0:
        click.secho(f"✅ Successfully created {success_count} file(s)", fg="green")
    if skip_count > 0:
        click.secho(f"⏭️  Skipped {skip_count} existing file(s)", fg="yellow")
        click.echo("   Use --force to overwrite existing config files")
    if error_count > 0:
        click.secho(f"❌ {error_count} error(s) occurred", fg="red")
        sys.exit(1)

    if success_count > 0:
        click.echo()
        click.echo("📝 Next steps:")
        click.echo("   1. Edit config/settings.json with your API keys")
        click.echo("   2. Edit config/endpoints.json to configure endpoints")
        if custom_dirs and Path("services_custom").is_dir():
            click.echo(
                "   3. Add custom services to services_custom/ and routers to routers_custom/"
            )
            click.echo("   4. Run: uv run apiary serve --reload")
        else:
            click.echo("   3. Run: uv run apiary serve --reload")


@cli.command()
@click.option(
    "--config-dir",
    default="config",
    help="Configuration directory path",
    show_default=True,
)
def validate_config(config_dir: str):
    """Validate API key configuration files."""
    import logging
    from pathlib import Path

    from core.api_key_validator import validate_all_api_keys

    # Setup logging for validation
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s", force=True
    )

    click.echo("🔍 Validating API key configurations...")
    click.echo()

    settings_path = Path(config_dir) / "settings.json"
    endpoints_path = Path(config_dir) / "endpoints.json"

    is_valid = validate_all_api_keys(str(settings_path), str(endpoints_path))

    click.echo()
    if is_valid:
        click.secho("✅ Configuration is valid", fg="green")
        sys.exit(0)
    else:
        click.secho("❌ Configuration has errors (see above)", fg="red")
        sys.exit(1)


@cli.command()
@click.option(
    "--config-dir",
    default="config",
    help="Configuration directory path",
    show_default=True,
)
@click.option(
    "--skip-import",
    is_flag=True,
    help="Skip application import test (only validate config)",
)
def test(config_dir: str, skip_import: bool):
    """Test application configuration and imports.

    Validates configuration files and tests that the application can be
    imported and initialized successfully. Use this before deploying updates
    to catch errors early.
    """
    import logging
    from pathlib import Path

    from core.api_key_validator import validate_all_api_keys

    # Setup logging for validation
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s", force=True
    )

    click.echo("🧪 Testing application configuration and imports...")
    click.echo()

    all_passed = True

    # Step 1: Validate configuration
    click.echo("1️⃣  Validating configuration...")
    settings_path = Path(config_dir) / "settings.json"
    endpoints_path = Path(config_dir) / "endpoints.json"

    is_valid = validate_all_api_keys(str(settings_path), str(endpoints_path))

    if is_valid:
        click.secho("   ✅ Configuration is valid", fg="green")
    else:
        click.secho("   ❌ Configuration has errors", fg="red")
        all_passed = False

    click.echo()

    # Step 2: Test application import
    if not skip_import:
        click.echo("2️⃣  Testing application import...")
        try:
            # Suppress logging during import to reduce noise
            logging.getLogger().setLevel(logging.ERROR)

            import fastapi

            from app import api  # noqa: F401

            if isinstance(api, fastapi.FastAPI):
                click.secho("   ✅ Application imports successfully", fg="green")
                click.secho("   ✅ FastAPI app created successfully", fg="green")
            else:
                click.secho(
                    "   ❌ Application import failed: not a FastAPI app", fg="red"
                )
                all_passed = False

            # Restore logging
            logging.getLogger().setLevel(logging.INFO)
        except ImportError as e:
            click.secho(f"   ❌ Import error: {e}", fg="red")
            all_passed = False
        except Exception as e:
            click.secho(f"   ❌ Application initialization failed: {e}", fg="red")
            all_passed = False
            import traceback

            click.echo("   Traceback:")
            for line in traceback.format_exc().splitlines():
                click.echo(f"   {line}")
    else:
        click.echo("2️⃣  Skipping application import test (--skip-import)")

    click.echo()

    # Summary
    if all_passed:
        click.secho("✅ All tests passed! Application is ready to deploy.", fg="green")
        sys.exit(0)
    else:
        click.secho("❌ Some tests failed. Fix errors before deploying.", fg="red")
        sys.exit(1)


@cli.command()
@click.option(
    "--config-dir",
    default="config",
    help="Configuration directory to backup",
    show_default=True,
)
@click.option(
    "--backup-dir",
    default="backups",
    help="Backup directory path",
    show_default=True,
)
@click.option(
    "--include-custom",
    is_flag=True,
    help="Also backup services_custom/ and routers_custom/ directories",
)
def backup(config_dir: str, backup_dir: str, include_custom: bool):
    """Backup configuration files and optionally custom code.

    Creates a timestamped backup of configuration files in backups/YYYYMMDD/.
    Use --include-custom to also backup services_custom/ and routers_custom/.
    """
    import shutil
    from datetime import datetime

    # Create timestamped backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(backup_dir) / timestamp

    click.echo(f"💾 Creating backup in {backup_path}/")

    try:
        backup_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        click.secho(f"❌ Failed to create backup directory: {e}", fg="red")
        sys.exit(1)

    success_count = 0
    skip_count = 0
    error_count = 0

    # Files to backup from config directory
    config_files = [
        "settings.json",
        "endpoints.json",
        "api_keys.txt",
    ]

    config_path = Path(config_dir)

    # Backup config files
    click.echo(f"\n📁 Backing up configuration from {config_dir}/...")
    for filename in config_files:
        source = config_path / filename
        if not source.exists():
            click.secho(f"   ⏭️  Skipping {filename} (does not exist)", fg="yellow")
            skip_count += 1
            continue

        try:
            dest = backup_path / "config" / filename
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            click.secho(f"   ✅ Backed up {filename}", fg="green")
            success_count += 1
        except Exception as e:
            click.secho(f"   ❌ Failed to backup {filename}: {e}", fg="red")
            error_count += 1

    # Backup additional key files if they exist
    for key_file in config_path.glob("*_keys.txt"):
        try:
            dest = backup_path / "config" / key_file.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(key_file, dest)
            click.secho(f"   ✅ Backed up {key_file.name}", fg="green")
            success_count += 1
        except Exception as e:
            click.secho(f"   ❌ Failed to backup {key_file.name}: {e}", fg="red")
            error_count += 1

    # Backup custom directories if requested
    if include_custom:
        click.echo("\n📁 Backing up custom code...")
        custom_dirs = ["services_custom", "routers_custom"]

        for custom_dir in custom_dirs:
            source_dir = Path(custom_dir)
            if not source_dir.exists():
                click.secho(
                    f"   ⏭️  Skipping {custom_dir}/ (does not exist)", fg="yellow"
                )
                skip_count += 1
                continue

            try:
                dest_dir = backup_path / custom_dir
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
                # Count files in the directory
                file_count = sum(1 for _ in dest_dir.rglob("*") if _.is_file())
                click.secho(
                    f"   ✅ Backed up {custom_dir}/ ({file_count} files)", fg="green"
                )
                success_count += 1
            except Exception as e:
                click.secho(f"   ❌ Failed to backup {custom_dir}/: {e}", fg="red")
                error_count += 1

    # Summary
    click.echo()
    if success_count > 0:
        click.secho(f"✅ Successfully backed up {success_count} item(s)", fg="green")
        click.secho(f"📦 Backup location: {backup_path}", fg="cyan")
    if skip_count > 0:
        click.secho(f"⏭️  Skipped {skip_count} missing item(s)", fg="yellow")
    if error_count > 0:
        click.secho(f"❌ {error_count} error(s) occurred", fg="red")
        sys.exit(1)

    # Show restore instructions
    if success_count > 0:
        click.echo()
        click.echo("📝 To restore from this backup:")
        click.echo(f"   cp -r {backup_path}/config/* config/")
        if include_custom:
            click.echo(f"   cp -r {backup_path}/services_custom/* services_custom/")
            click.echo(f"   cp -r {backup_path}/routers_custom/* routers_custom/")


@cli.group()
def docker():
    """Manage the application Docker container via docker compose."""
    pass


@docker.command()
@click.option("--build", is_flag=True, help="Rebuild images before starting")
def up(build: bool) -> None:
    """Start the application container in the background.

    Pass --build to rebuild the image first (required after code changes
    outside of the mounted config/ and services/ volumes).
    """
    cmd = ["docker", "compose", "up", "-d"]
    if build:
        cmd.append("--build")
    run_command(cmd, "Starting Docker container")


@docker.command()
def down() -> None:
    """Stop and remove the application container."""
    run_command(["docker", "compose", "down"], "Stopping Docker container")


@docker.command()
def restart() -> None:
    """Restart the running application container.

    Use this after editing files in the mounted config/ or services/ volumes
    so the application picks up the changes.
    """
    run_command(["docker", "compose", "restart"], "Restarting Docker container")


@cli.command()
def clean():
    """Clean up generated files and caches."""
    import shutil

    patterns = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".pytest_cache",
        ".ruff_cache",
        "htmlcov",
        ".coverage",
        "site",
        "*.egg-info",
    ]

    click.echo("🧹 Cleaning up generated files...")

    for pattern in patterns:
        if "*" in pattern:
            # Handle file patterns
            for path in Path(".").rglob(pattern):
                if path.is_file():
                    path.unlink()
                    click.echo(f"   Removed: {path}")
        else:
            # Handle directory patterns
            for path in Path(".").rglob(pattern):
                if path.is_dir():
                    shutil.rmtree(path)
                    click.echo(f"   Removed: {path}")
                elif path.is_file():
                    path.unlink()
                    click.echo(f"   Removed: {path}")

    click.secho("✅ Cleanup complete", fg="green")


if __name__ == "__main__":
    cli()
