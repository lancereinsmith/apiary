"""API key management with file watching and caching."""

import logging
import threading
from pathlib import Path
from typing import Any

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from core.api_key_validator import validate_api_key_source

logger = logging.getLogger(__name__)


class APIKeyFileHandler(FileSystemEventHandler):
    """File system event handler for API key files."""

    def __init__(self, manager: "APIKeyManager", file_path: Path):
        """Initialize the handler.

        Args:
            manager: The APIKeyManager instance to notify
            file_path: Path to the API key file being watched
        """
        self.manager = manager
        self.file_path = file_path

    def on_modified(self, event: FileSystemEvent):
        """Handle file modification events.

        Args:
            event: The file system event
        """
        src_path = (
            event.src_path.decode()
            if isinstance(event.src_path, bytes)
            else event.src_path
        )
        if not event.is_directory and Path(src_path) == self.file_path:
            logger.info(f"API key file modified: {self.file_path}")
            self.manager.reload_file(str(self.file_path))


class APIKeyManager:
    """Manages API keys from strings and files with automatic reloading."""

    def __init__(self):
        """Initialize the API key manager."""
        self._keys_cache: dict[str, set[str]] = {}
        self._file_watchers: dict[str, Any] = {}
        self._lock = threading.Lock()

    def load_keys(self, source: str, source_id: str = "default") -> set[str]:
        """Load API keys from a string or file.

        Args:
            source: Either comma-separated API keys or a file path
            source_id: Identifier for this key source (for caching)

        Returns:
            Set of valid API keys

        Raises:
            ValueError: If the source appears to be a file path but doesn't exist
        """
        if not source or not source.strip():
            return set()

        # Validate the source
        validation = validate_api_key_source(source, source_id)

        # Log warnings
        for warning in validation["warnings"]:
            logger.warning(warning)

        # Raise error if invalid
        if not validation["valid"]:
            error_msg = "; ".join(validation["errors"])
            logger.error(f"Invalid API key source '{source_id}': {error_msg}")
            raise ValueError(f"Invalid API key source: {error_msg}")

        # Load based on type
        if validation["type"] == "file":
            return self._load_from_file(validation["path"], source_id)
        else:
            # Treat as comma-separated string
            return self._parse_key_string(source)

    def _parse_key_string(self, keys_string: str) -> set[str]:
        """Parse comma-separated API keys.

        Args:
            keys_string: Comma-separated API keys

        Returns:
            Set of API keys
        """
        return {key.strip() for key in keys_string.split(",") if key.strip()}

    def _load_from_file(self, file_path: Path, source_id: str) -> set[str]:
        """Load API keys from a file.

        Args:
            file_path: Path to the file containing API keys
            source_id: Identifier for caching

        Returns:
            Set of API keys from the file
        """
        with self._lock:
            cache_key = f"file:{file_path}"

            # Start watching the file if not already watching
            if cache_key not in self._file_watchers:
                self._start_watching_file(file_path)

            # Load keys from file
            keys = self._read_keys_from_file(file_path)
            self._keys_cache[cache_key] = keys

            logger.info(
                f"Loaded {len(keys)} API key(s) from file: {file_path} "
                f"(id: {source_id})"
            )
            return keys

    def _read_keys_from_file(self, file_path: Path) -> set[str]:
        """Read API keys from a file.

        Each line in the file is treated as a separate API key.
        Empty lines and lines starting with # are ignored.

        Args:
            file_path: Path to the file

        Returns:
            Set of API keys
        """
        keys = set()
        try:
            with open(file_path) as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith("#"):
                        keys.add(line)
        except Exception as e:
            logger.error(f"Failed to read API keys from {file_path}: {e}")

        return keys

    def _start_watching_file(self, file_path: Path):
        """Start watching a file for changes.

        Args:
            file_path: Path to the file to watch
        """
        cache_key = f"file:{file_path}"

        try:
            observer = Observer()
            event_handler = APIKeyFileHandler(self, file_path)

            # Watch the directory containing the file
            watch_path = file_path.parent
            observer.schedule(event_handler, str(watch_path), recursive=False)
            observer.start()

            self._file_watchers[cache_key] = observer
            logger.info(f"Started watching API key file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to start watching file {file_path}: {e}")

    def reload_file(self, file_path: str):
        """Reload API keys from a file.

        Args:
            file_path: Path to the file to reload
        """
        path = Path(file_path)
        cache_key = f"file:{path}"

        with self._lock:
            if cache_key in self._keys_cache:
                keys = self._read_keys_from_file(path)
                self._keys_cache[cache_key] = keys
                logger.info(f"Reloaded {len(keys)} API key(s) from {file_path}")

    def get_cached_keys(self, source: str) -> set[str] | None:
        """Get cached keys for a source.

        Args:
            source: The source string (file path or keys)

        Returns:
            Set of keys if cached, None otherwise
        """
        source_path = Path(source.strip())
        if source_path.exists() and source_path.is_file():
            cache_key = f"file:{source_path}"
            with self._lock:
                return self._keys_cache.get(cache_key)
        return None

    def validate_key(self, api_key: str, *sources: str) -> bool:
        """Validate an API key against one or more sources.

        Args:
            api_key: The API key to validate
            *sources: One or more sources (file paths or key strings)

        Returns:
            True if the key is valid in any source, False otherwise
        """
        if not api_key:
            return False

        for source in sources:
            if not source:
                continue

            keys = self.load_keys(source)
            if api_key in keys:
                return True

        return False

    def shutdown(self):
        """Stop all file watchers."""
        with self._lock:
            for observer in self._file_watchers.values():
                observer.stop()
                observer.join()
            self._file_watchers.clear()
            logger.info("API key file watchers stopped")


# Global instance
_api_key_manager: APIKeyManager | None = None


def get_api_key_manager() -> APIKeyManager:
    """Get the global API key manager instance.

    Returns:
        The APIKeyManager instance
    """
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = APIKeyManager()
    return _api_key_manager
