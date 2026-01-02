"""Main application entry point."""

import logging
from contextlib import asynccontextmanager

import fastapi
import uvicorn
from fastapi.responses import JSONResponse
from starlette.staticfiles import StaticFiles

# Import services to register them
import services  # noqa: F401
from __version__ import __version__
from config import initialize_settings
from core import APIException
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
from routers import auth, endpoints, health, home, metrics

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
    yield
    # Shutdown
    logger.info("Application shutting down...")
    await http_client_dependency.close()


# Create FastAPI app
api = fastapi.FastAPI(
    title="Apiary",
    description="Personal API service for various projects",
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


def configure():
    """Configure the application."""
    configure_exception_handlers()
    configure_middleware()
    configure_routing()


def configure_exception_handlers():
    """Configure global exception handlers."""

    @api.exception_handler(APIException)
    async def api_exception_handler(request: fastapi.Request, exc: APIException):
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


def configure_middleware():
    """Configure application middleware."""
    # CORS must be added first
    configure_cors(api, allowed_origins=None)  # Allow all origins for now

    # Add other middleware (order matters - first added is last executed)
    api.add_middleware(SecurityHeadersMiddleware)
    api.add_middleware(RequestValidationMiddleware)  # Request validation
    api.add_middleware(MetricsMiddleware)  # Collect metrics
    api.add_middleware(RateLimitMiddleware)  # Rate limiting
    api.add_middleware(RequestIDMiddleware)
    api.add_middleware(LoggingMiddleware)


def configure_routing():
    """Configure application routes."""
    api.mount("/static", StaticFiles(directory="static"), name="static")

    # Conditionally include landing page based on settings
    if settings.enable_landing_page:
        api.include_router(home.router)

    api.include_router(health.router)
    api.include_router(metrics.router)
    api.include_router(auth.router)
    api.include_router(endpoints.router)

    # Load and register configurable endpoints
    dynamic_router = DynamicRouter(api)
    dynamic_router.load_and_register()


if __name__ == "__main__":
    configure()
    uvicorn.run(api, port=8000, host="127.0.0.1")
else:
    configure()
