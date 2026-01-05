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
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--coverage", "-c", is_flag=True, help="Run with coverage")
def test(verbose: bool, coverage: bool):
    """Run the test suite."""
    cmd = ["pytest"]
    if verbose:
        cmd.append("-v")
    if coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
    run_command(cmd, "Running tests")


@cli.command()
@click.option("--check", is_flag=True, help="Check only, don't modify files")
def format_code(check: bool):
    """Format code with Black."""
    cmd = ["black"]
    if check:
        cmd.append("--check")
    cmd.append(".")
    run_command(cmd, "Formatting code with Black")


@cli.command()
@click.option("--fix", is_flag=True, help="Auto-fix issues where possible")
def lint(fix: bool):
    """Run Ruff linter."""
    cmd = ["ruff", "check"]
    if fix:
        cmd.append("--fix")
    cmd.append(".")
    run_command(cmd, "Running Ruff linter", check=False)


@cli.command()
def typecheck():
    """Run MyPy type checker."""
    cmd = ["mypy", ".", "--ignore-missing-imports"]
    run_command(cmd, "Running MyPy type checker", check=False)


@cli.command()
@click.option("--html", is_flag=True, default=True, help="Generate HTML report")
@click.option("--open-browser", "-o", is_flag=True, help="Open HTML report in browser")
def coverage(html: bool, open_browser: bool):
    """Run tests with coverage report."""
    cmd = ["pytest", "--cov=.", "--cov-report=term"]
    if html:
        cmd.append("--cov-report=html")

    exit_code = run_command(cmd, "Running tests with coverage")

    if exit_code == 0 and html:
        click.echo("📊 Coverage report generated in htmlcov/index.html")
        if open_browser:
            import webbrowser

            report_path = Path("htmlcov/index.html").absolute()
            webbrowser.open(f"file://{report_path}")


@cli.command()
@click.option("--fix", is_flag=True, help="Auto-fix issues where possible")
def check_all(fix: bool):
    """Run all checks: format, lint, typecheck, and tests."""
    click.echo("=" * 60)
    click.secho("Running all checks...", fg="blue", bold=True)
    click.echo("=" * 60)

    results = []

    # Format check
    cmd = ["black", "--check" if not fix else "", "."]
    cmd = [c for c in cmd if c]  # Remove empty strings
    results.append(("Format", run_command(cmd, "Checking code format", check=False)))

    # Lint
    cmd = ["ruff", "check"]
    if fix:
        cmd.append("--fix")
    cmd.append(".")
    results.append(("Lint", run_command(cmd, "Running linter", check=False)))

    # Type check
    results.append(
        (
            "Type Check",
            run_command(
                ["mypy", ".", "--ignore-missing-imports"],
                "Running type checker",
                check=False,
            ),
        )
    )

    # Tests
    results.append(("Tests", run_command(["pytest"], "Running tests", check=False)))

    # Summary
    click.echo("\n" + "=" * 60)
    click.secho("Summary:", fg="blue", bold=True)
    click.echo("=" * 60)

    all_passed = True
    for name, exit_code in results:
        status = "✅ PASSED" if exit_code == 0 else "❌ FAILED"
        color = "green" if exit_code == 0 else "red"
        click.echo(f"{name:15} {click.style(status, fg=color)}")
        if exit_code != 0:
            all_passed = False

    if all_passed:
        click.secho("\n🎉 All checks passed!", fg="green", bold=True)
    else:
        click.secho("\n⚠️  Some checks failed", fg="red", bold=True)
        sys.exit(1)


@cli.command()
@click.option("--port", "-p", default=8000, help="Port to serve on")
def docs_serve(port: int):
    """Serve documentation locally."""
    cmd = ["mkdocs", "serve", "--dev-addr", f"127.0.0.1:{port}"]
    click.echo(f"📚 Serving documentation at http://127.0.0.1:{port}")
    run_command(cmd, "Serving documentation")


@cli.command()
def docs_build():
    """Build documentation."""
    cmd = ["mkdocs", "build"]
    run_command(cmd, "Building documentation")
    click.echo("📚 Documentation built in site/")


@cli.command()
@click.option("--message", "-m", help="Deployment message")
def docs_deploy(message: str):
    """Deploy documentation to GitHub Pages."""
    cmd = ["mkdocs", "gh-deploy"]
    if message:
        cmd.extend(["--message", message])
    run_command(cmd, "Deploying documentation to GitHub Pages")


@cli.command()
@click.argument("host", default="127.0.0.1")
@click.argument("port", type=int, default=8000)
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def serve(host: str, port: int, reload: bool):
    """Start the API server."""
    cmd = ["uvicorn", "app:api", f"--host={host}", f"--port={port}"]
    if reload:
        cmd.append("--reload")
    click.echo(f"🚀 Starting Apiary API server at http://{host}:{port}")
    run_command(cmd, "Starting server")


@cli.command()
def clean():
    """Clean up generated files and caches."""
    import shutil

    patterns = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".pytest_cache",
        ".mypy_cache",
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

