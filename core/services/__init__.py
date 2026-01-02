"""Service registry and factory."""

from typing import Dict, Optional, Type

from core.services.base import BaseService

# Service registry
_service_registry: Dict[str, Type[BaseService]] = {}


def register_service(name: str, service_class: Type[BaseService]):
    """Register a service class.

    Args:
        name: Service name
        service_class: Service class to register
    """
    _service_registry[name.lower()] = service_class


def get_service(name: str) -> Optional[Type[BaseService]]:
    """Get a service class by name.

    Args:
        name: Service name

    Returns:
        Service class or None if not found
    """
    return _service_registry.get(name.lower())


def list_services() -> list[str]:
    """List all registered service names.

    Returns:
        List of service names
    """
    return list(_service_registry.keys())
