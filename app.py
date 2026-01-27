"""FastAPI application factory and configuration."""

import importlib
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import fastapi
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles

# Import services to register them
import services  # noqa: F401
from __version__ import __version__
from config import initialize_settings
from core import APIError
from core.dependencies import http_client_dependency
from core.logging_config import setup_logging
from core.metrics import MetricsMiddleware
from core.middleware import (
    LoggingMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
    configure_cors,
)
from core.rate_limiter import RateLimitMiddleware
from core.request_validation import RequestValidationMiddleware
from core.router_factory import DynamicRouter


def create_app() -> fastapi.FastAPI:
    """Create and configure the FastAPI application.

    This function initializes settings, sets up logging, creates the FastAPI
    app instance, and configures all middleware, exception handlers, and routes.

    Returns:
        Configured FastAPI application instance.
    """
    # Load environment variables from .env file if it exists
    env_file = Path(".env")
    if env_file.exists():
        load_dotenv(env_file)

    # Initialize settings
    settings = initialize_settings()

    # Setup logging
    setup_logging(level="INFO")

    # Get logger after setup
    logger = logging.getLogger(__name__)

    @asynccontextmanager
    async def lifespan(app: fastapi.FastAPI):
        """Application lifespan manager for startup/shutdown events."""
        # Startup
        logger.info("Application starting up...")

        # Validate API key configurations
        from core.api_key_validator import validate_all_api_keys

        if not validate_all_api_keys():
            logger.warning(
                "API key configuration validation failed. "
                "Check logs for details. Server will start but auth may not work."
            )

        yield
        # Shutdown
        logger.info("Application shutting down...")
        await http_client_dependency.close()

        # Shutdown API key file watchers
        from core.api_key_manager import get_api_key_manager

        get_api_key_manager().shutdown()

    # Create FastAPI app
    api = fastapi.FastAPI(
        title="Apiary",
        description="Personal API service for various projects",
        version=__version__,
        lifespan=lifespan,
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_redoc else None,
        openapi_url="/openapi.json" if settings.enable_openapi else None,
    )

    # Configure the application
    _configure_exception_handlers(api)
    _configure_middleware(api)
    _configure_routing(api, settings)

    return api


def _configure_exception_handlers(api: fastapi.FastAPI) -> None:
    """Configure global exception handlers."""

    @api.exception_handler(APIError)
    async def api_exception_handler(request: fastapi.Request, exc: APIError):
        """Handle API exceptions."""
        request_id = getattr(request.state, "request_id", "unknown")

        error_response = {
            "error": {
                "message": exc.message,
                "status_code": exc.status_code,
                "error_code": exc.error_code,
                "request_id": request_id,
            }
        }

        # Add details if present
        if exc.details:
            error_response["error"]["details"] = exc.details

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response,
        )

    @api.exception_handler(Exception)
    async def general_exception_handler(request: fastapi.Request, exc: Exception):
        """Handle general exceptions."""
        request_id = getattr(request.state, "request_id", "unknown")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": "Internal server error",
                    "status_code": 500,
                    "request_id": request_id,
                }
            },
        )


def _configure_middleware(api: fastapi.FastAPI) -> None:
    """Configure application middleware."""
    # CORS must be added first
    configure_cors(api, allowed_origins=None)  # Allow all origins for now

    # Add other middleware (order matters - first added is last executed)
    api.add_middleware(SecurityHeadersMiddleware)  # type: ignore[invalid-argument-type]
    api.add_middleware(RequestValidationMiddleware)  # type: ignore[invalid-argument-type]  # Request validation
    api.add_middleware(MetricsMiddleware)  # type: ignore[invalid-argument-type]  # Collect metrics
    api.add_middleware(RateLimitMiddleware)  # type: ignore[invalid-argument-type]  # Rate limiting
    api.add_middleware(RequestIDMiddleware)  # type: ignore[invalid-argument-type]
    api.add_middleware(LoggingMiddleware)  # type: ignore[invalid-argument-type]


def _discover_routers() -> dict[str, fastapi.APIRouter]:
    """Auto-discover routers from routers/ and routers_custom/.

    Scans routers/ first (built-in), then routers_custom/ (user extensions).
    Custom routers override built-ins when names collide. The routers_custom/
    directory is gitignored so custom code is never overwritten by git pull.

    Returns:
        Dictionary mapping router names to router instances.
    """
    logger = logging.getLogger(__name__)
    discovered_routers: dict[str, fastapi.APIRouter] = {}

    for package_name, routers_dir in [
        ("routers", Path("routers")),
        ("routers_custom", Path("routers_custom")),
    ]:
        if not routers_dir.is_dir():
            continue

        for router_file in routers_dir.glob("*.py"):
            if router_file.name.startswith("_") or router_file.name == "__init__.py":
                continue

            module_name = router_file.stem

            try:
                module = importlib.import_module(f"{package_name}.{module_name}")

                if hasattr(module, "router") and isinstance(
                    module.router, fastapi.APIRouter
                ):
                    discovered_routers[module_name] = module.router
                    logger.debug(f"Discovered router: {module_name} ({package_name})")
                else:
                    logger.debug(
                        f"Module {package_name}.{module_name} has no router attribute"
                    )
            except Exception as e:
                logger.error(
                    f"Failed to import {package_name}.{module_name}: {e}", exc_info=True
                )

    if not discovered_routers and not Path("routers").is_dir():
        logger.warning("Routers directory not found")

    return discovered_routers


def _configure_routing(api: fastapi.FastAPI, settings) -> None:
    """Configure application routes."""
    logger = logging.getLogger(__name__)

    api.mount("/static", StaticFiles(directory="static"), name="static")

    # Auto-discover available routers
    available_routers = _discover_routers()

    # Special handling for home router (landing page)
    if settings.enable_landing_page and "home" in available_routers:
        api.include_router(available_routers["home"])
        logger.info("Enabled router: home (landing page)")

    # Load enabled routers based on settings
    for router_name in settings.enabled_routers:
        if router_name in available_routers:
            api.include_router(available_routers[router_name])
            logger.info(f"Enabled router: {router_name}")
        else:
            logger.warning(
                f"Router '{router_name}' not found. "
                f"Available routers: {list(available_routers.keys())}"
            )

    # Load and register configurable endpoints
    dynamic_router = DynamicRouter(api)
    dynamic_router.load_and_register()


# Create the application instance
# This can be imported as: from app import api
api = create_app()
