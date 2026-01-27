"""Dynamic router factory for configurable endpoints."""

import logging
from typing import Any

import fastapi
import httpx
from fastapi import Depends

from config.endpoint_config import EndpointConfig, load_endpoints_config
from core.auth.authentication import AuthenticatedUser
from core.auth.authorization import create_auth_dependency, require_auth
from core.dependencies import http_client_dependency
from core.services import get_service
from core.services.base import BaseService

logger = logging.getLogger(__name__)


class DynamicRouter:
    """Dynamic router for configurable endpoints."""

    def __init__(self, app: fastapi.FastAPI):
        """Initialize dynamic router.

        Args:
            app: FastAPI application instance
        """
        self.app = app
        self.registered_endpoints: list[str] = []

    def register_endpoint(self, config: EndpointConfig):
        """Register a single endpoint from configuration.

        Args:
            config: Endpoint configuration
        """
        if not config.enabled:
            logger.debug(f"Skipping disabled endpoint: {config.path}")
            return

        # Get service class
        service_class = get_service(config.service)
        if not service_class:
            logger.warning(
                f"Service '{config.service}' not found for endpoint {config.path}"
            )
            return

        # Create endpoint handler
        handler = self._create_handler(config, service_class)

        # Register route
        route_method = getattr(self.app, config.method.value.lower())
        route_kwargs = {
            "path": config.path,
            "summary": config.summary or config.description,
            "description": config.description,
            "tags": config.tags or ["configurable"],
        }

        # Add response model if specified
        if config.response_model:
            # For now, we'll use dict as response model
            # Can be extended to use actual Pydantic models
            route_kwargs["response_model"] = dict

        # Register the route
        route_method(**route_kwargs)(handler)

        endpoint_id = f"{config.method.value} {config.path}"
        self.registered_endpoints.append(endpoint_id)
        logger.info(f"Registered configurable endpoint: {endpoint_id}")

    def _create_handler(self, config: EndpointConfig, service_class: type[BaseService]):
        """Create an endpoint handler function.

        Args:
            config: Endpoint configuration
            service_class: Service class to use

        Returns:
            Handler function
        """
        # Create handler function with proper dependencies based on auth requirement
        if config.requires_auth:
            # Use endpoint-specific auth if keys are provided, otherwise use default
            if config.api_keys:
                auth_dependency = create_auth_dependency(config.api_keys)
                logger.info(f"Endpoint {config.path} using endpoint-specific API keys")
            else:
                auth_dependency = require_auth

            async def endpoint_handler(
                request: fastapi.Request,
                client: httpx.AsyncClient = Depends(http_client_dependency),
                user: AuthenticatedUser = Depends(auth_dependency),
            ) -> dict[str, Any]:
                """Dynamic endpoint handler (authenticated)."""
                return await self._handle_endpoint(
                    request, config, service_class, client
                )
        else:

            async def endpoint_handler(
                request: fastapi.Request,
                client: httpx.AsyncClient = Depends(http_client_dependency),
            ) -> dict[str, Any]:
                """Dynamic endpoint handler (public)."""
                return await self._handle_endpoint(
                    request, config, service_class, client
                )

        return endpoint_handler

    async def _handle_endpoint(
        self,
        request: fastapi.Request,
        config: EndpointConfig,
        service_class: type[BaseService],
        client: httpx.AsyncClient,
    ) -> dict[str, Any]:
        """Handle endpoint request.

        Args:
            request: FastAPI request object
            config: Endpoint configuration
            service_class: Service class to use
            client: HTTP client

        Returns:
            Service response
        """
        # Create service instance
        service = service_class(http_client=client)

        try:
            # Extract parameters from request
            parameters = self._extract_parameters(request, config)

            # Call service
            result = await service.call(parameters)

            return result
        finally:
            # Cleanup service
            await service.cleanup()

    def _extract_parameters(
        self, request: fastapi.Request, config: EndpointConfig
    ) -> dict[str, Any]:
        """Extract parameters from request based on configuration.

        Args:
            request: FastAPI request object
            config: Endpoint configuration

        Returns:
            Extracted parameters
        """
        parameters: dict[str, Any] = {}

        if config.parameters:
            # Use configured parameter mapping
            for param_name, param_config in config.parameters.items():
                if isinstance(param_config, dict):
                    # Parameter mapping configuration
                    source = param_config.get("source", "query")  # query, path, body
                    key = param_config.get("key", param_name)

                    if source == "query":
                        parameters[param_name] = request.query_params.get(key)
                    elif source == "path":
                        parameters[param_name] = request.path_params.get(key)
                    # body would need more complex handling
                else:
                    # Simple value
                    parameters[param_name] = param_config

        # Also include query parameters if not explicitly mapped
        if not config.parameters:
            parameters.update(dict(request.query_params))

        return parameters

    def load_and_register(self, config_path: str = "config/endpoints.json"):
        """Load configuration and register all endpoints.

        Args:
            config_path: Path to endpoints configuration file
        """
        try:
            config = load_endpoints_config(config_path)
            for endpoint_config in config.endpoints:
                try:
                    self.register_endpoint(endpoint_config)
                except Exception as e:
                    logger.error(
                        f"Failed to register endpoint {endpoint_config.path}: {e}",
                        exc_info=True,
                    )
        except Exception as e:
            logger.error(f"Failed to load endpoint configuration: {e}", exc_info=True)
