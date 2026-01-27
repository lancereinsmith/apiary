"""API key configuration validation."""

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class APIKeyValidationError(Exception):
    """Raised when API key configuration is invalid."""

    pass


def validate_api_key_source(source: str, source_name: str = "api_keys") -> dict:
    """Validate an API key source (string or file path).

    Args:
        source: The API key source (comma-separated keys or file path)
        source_name: Name of the source for error messages

    Returns:
        Dictionary with validation results:
        {
            "valid": bool,
            "type": "file" | "string",
            "path": Optional[Path],
            "warnings": list[str],
            "errors": list[str]
        }

    Raises:
        APIKeyValidationError: If the source is invalid
    """
    result: dict[str, Any] = {
        "valid": True,
        "type": "string",
        "path": None,
        "warnings": [],
        "errors": [],
    }

    if not source or not source.strip():
        result["errors"].append(f"{source_name}: Empty or whitespace-only value")
        result["valid"] = False
        return result

    source = source.strip()

    # Check if it looks like a file path
    looks_like_path = (
        "/" in source or source.endswith(".txt") or source.endswith(".keys")
    )

    # Try to treat as file path
    try:
        path = Path(source)

        # If the path exists and is a file, it's definitely a file source
        if path.exists():
            if path.is_file():
                result["type"] = "file"
                result["path"] = path

                # Check file readability
                try:
                    with open(path) as f:
                        lines = f.readlines()

                    # Count valid keys
                    key_count = sum(
                        1
                        for line in lines
                        if line.strip() and not line.strip().startswith("#")
                    )

                    if key_count == 0:
                        result["warnings"].append(
                            f"{source_name}: File '{source}' contains no valid API keys"
                        )

                    logger.debug(
                        f"{source_name}: File '{source}' contains {key_count} key(s)"
                    )

                except Exception as e:
                    result["errors"].append(
                        f"{source_name}: Cannot read file '{source}': {e}"
                    )
                    result["valid"] = False

            else:
                result["errors"].append(
                    f"{source_name}: Path '{source}' exists but is not a file"
                )
                result["valid"] = False

        else:
            # Path doesn't exist
            if looks_like_path:
                # It looks like a file path but doesn't exist - this is an error
                result["errors"].append(
                    f"{source_name}: File '{source}' does not exist. "
                    f"If this is meant to be an API key, it looks like a file path."
                )
                result["valid"] = False
            else:
                # Treat as comma-separated string
                result["type"] = "string"
                keys = [k.strip() for k in source.split(",") if k.strip()]

                if len(keys) == 0:
                    result["errors"].append(
                        f"{source_name}: No valid keys found in string"
                    )
                    result["valid"] = False
                else:
                    # Check for suspiciously short or long keys
                    for key in keys:
                        if len(key) < 8:
                            result["warnings"].append(
                                f"{source_name}: Key '{key}' is very short "
                                "(<8 chars). Consider using stronger keys."
                            )
                        if len(key) > 200:
                            result["warnings"].append(
                                f"{source_name}: Key starts with '{key[:30]}...' "
                                "is very long. This might be a mistake."
                            )

                    logger.debug(f"{source_name}: Contains {len(keys)} inline key(s)")

    except Exception as e:
        result["errors"].append(f"{source_name}: Validation error: {e}")
        result["valid"] = False

    return result


def validate_settings_api_keys(settings_path: str = "config/settings.json") -> bool:
    """Validate API keys in settings file.

    Args:
        settings_path: Path to settings.json file

    Returns:
        True if valid, False otherwise
    """
    import json

    try:
        path = Path(settings_path)
        if not path.exists():
            logger.warning(f"Settings file not found: {settings_path}")
            return True  # Not an error if file doesn't exist

        with open(path) as f:
            data = json.load(f)

        api_keys = data.get("api_keys", "")
        if not api_keys:
            logger.info("No API keys configured in settings (authentication disabled)")
            return True

        result = validate_api_key_source(api_keys, "settings.api_keys")

        # Log warnings
        for warning in result["warnings"]:
            logger.warning(warning)

        # Log errors
        for error in result["errors"]:
            logger.error(error)

        return result["valid"]

    except Exception as e:
        logger.error(f"Failed to validate settings API keys: {e}")
        return False


def validate_endpoints_api_keys(
    endpoints_path: str = "config/endpoints.json",
) -> bool:
    """Validate API keys in endpoints file.

    Args:
        endpoints_path: Path to endpoints.json file

    Returns:
        True if valid, False otherwise
    """
    import json

    try:
        path = Path(endpoints_path)
        if not path.exists():
            logger.warning(f"Endpoints file not found: {endpoints_path}")
            return True  # Not an error if file doesn't exist

        with open(path) as f:
            data = json.load(f)

        endpoints = data.get("endpoints", [])
        all_valid = True

        for i, endpoint in enumerate(endpoints):
            endpoint_id = endpoint.get("path", f"endpoint[{i}]")
            api_keys = endpoint.get("api_keys")

            if api_keys:
                result = validate_api_key_source(
                    api_keys, f"endpoints[{endpoint_id}].api_keys"
                )

                # Log warnings
                for warning in result["warnings"]:
                    logger.warning(warning)

                # Log errors
                for error in result["errors"]:
                    logger.error(error)

                if not result["valid"]:
                    all_valid = False

        return all_valid

    except Exception as e:
        logger.error(f"Failed to validate endpoints API keys: {e}")
        return False


def validate_all_api_keys(
    settings_path: str = "config/settings.json",
    endpoints_path: str = "config/endpoints.json",
) -> bool:
    """Validate all API key configurations.

    Args:
        settings_path: Path to settings.json file
        endpoints_path: Path to endpoints.json file

    Returns:
        True if all configurations are valid, False otherwise
    """
    logger.info("Validating API key configurations...")

    settings_valid = validate_settings_api_keys(settings_path)
    endpoints_valid = validate_endpoints_api_keys(endpoints_path)

    if settings_valid and endpoints_valid:
        logger.info("✅ All API key configurations are valid")
        return True
    else:
        logger.error("❌ API key configuration validation failed")
        return False
