"""Version information for Apiary."""

try:
    from importlib.metadata import version

    __version__ = version("apiary")
except Exception:
    # Fallback for development/editable installs
    __version__ = "0.1.0-dev"
