"""Service modules for business logic.

This module automatically discovers and registers all services from the
services/ directory and, if present, services_custom/. Services are classes
that inherit from BaseService and can optionally define a 'service_name' class
attribute to control their registration name.

Services in services_custom/ are discovered after services/, so a custom
service with the same name will override a built-in. The services_custom/
directory is gitignored so custom code is never overwritten by git pull.

Services are always registered if discovered. Control which endpoints use
them via the 'enabled' field in config/endpoints.json.
"""

import importlib
import inspect
import logging
from pathlib import Path

from core.services import register_service
from core.services.base import BaseService

logger = logging.getLogger(__name__)


def _register_services_from_directory(package_name: str, search_dir: Path) -> list[str]:
    """Discover and register services from a directory.

    Args:
        package_name: Python package name for imports (e.g., 'services' or 'services_custom')
        search_dir: Directory to scan for .py files

    Returns:
        List of registered service names
    """
    registered: list[str] = []

    for service_file in search_dir.glob("*.py"):
        if service_file.name.startswith("_") or service_file.name == "__init__.py":
            continue

        module_name = service_file.stem

        try:
            module = importlib.import_module(f"{package_name}.{module_name}")

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseService) and obj is not BaseService:
                    service_name: str
                    if hasattr(obj, "service_name") and obj.service_name:
                        service_name = str(obj.service_name)
                    else:
                        service_name = module_name.replace("_service", "")

                    register_service(service_name, obj)
                    registered.append(service_name)
                    logger.debug(
                        f"Registered service '{service_name}' from {package_name}.{module_name}.{name}"
                    )

        except Exception as e:
            logger.error(
                f"Failed to import {package_name}.{module_name}: {e}", exc_info=True
            )

    return registered


def _discover_and_register_services() -> None:
    """Discover and register services from services/ and services_custom/.

    Scans services/ first (built-in), then services_custom/ (user extensions).
    Custom services override built-ins when names collide. The services_custom/
    directory is gitignored so it is never overwritten by git pull.

    Service names are determined by:
    1. The 'service_name' class attribute (if defined)
    2. The filename without '_service.py' suffix (fallback)
    """
    base_dir = Path(__file__).parent.parent
    services_dir = base_dir / "services"
    services_custom_dir = base_dir / "services_custom"

    all_registered: list[str] = []

    # Built-in services first
    all_registered.extend(_register_services_from_directory("services", services_dir))

    # Custom services second (override built-ins; directory is gitignored)
    if services_custom_dir.is_dir():
        custom = _register_services_from_directory(
            "services_custom", services_custom_dir
        )
        all_registered.extend(custom)
        if custom:
            logger.info(f"Loaded {len(custom)} custom service(s) from services_custom/")

    if all_registered:
        logger.info(f"Auto-registered {len(all_registered)} services: {all_registered}")
    else:
        logger.warning("No services were discovered in services/ or services_custom/")


# Auto-discover and register services on import
_discover_and_register_services()
