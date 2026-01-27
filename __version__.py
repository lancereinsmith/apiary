"""Version information for Apiary."""

try:
    from importlib.metadata import version

    __version__ = version("apiary")
except Exception:
    # Fallback: read directly from pyproject.toml for development
    try:
        import tomllib
        from pathlib import Path

        pyproject_path = Path(__file__).parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            pyproject = tomllib.load(f)
        __version__ = pyproject["project"]["version"]
    except Exception:
        # Last resort fallback
        __version__ = "0.0.0-dev"
