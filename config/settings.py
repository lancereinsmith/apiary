"""Application settings using Pydantic Settings."""

import json
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""

    # API authentication keys (comma-separated list)
    api_keys: str = Field(
        default="",
        description="Comma-separated list of valid API keys for authentication",
    )

    # UI configuration
    enable_landing_page: bool = Field(
        default=True,
        description="Enable the HTML landing page at /",
    )

    # API Documentation configuration
    enable_docs: bool = Field(
        default=True,
        description="Enable Swagger UI documentation at /docs",
    )
    enable_redoc: bool = Field(
        default=True,
        description="Enable ReDoc documentation at /redoc",
    )
    enable_openapi: bool = Field(
        default=True,
        description="Enable OpenAPI JSON schema at /openapi.json",
    )

    # Router configuration
    enabled_routers: list[str] = Field(
        default=["health", "metrics", "auth", "endpoints"],
        description="List of built-in routers (health, metrics, auth, endpoints)",
    )

    # Rate limiting configuration
    rate_limit_enabled: bool = Field(
        default=True,
        description="Enable rate limiting",
    )
    rate_limit_per_minute: int = Field(
        default=60,
        description="Rate limit per minute for public endpoints",
    )
    rate_limit_per_minute_authenticated: int = Field(
        default=300,
        description="Rate limit per minute for authenticated endpoints",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @classmethod
    def from_json_file(cls, file_path: Path) -> "Settings":
        """Load settings from a JSON file."""
        if not file_path.exists():
            raise FileNotFoundError(
                f"Settings file not found: {file_path}. "
                f"Please see config/settings_template.json"
            )

        with open(file_path) as f:
            data = json.load(f)

        return cls(**data)


# Global settings instance (will be initialized on startup)
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get the application settings instance."""
    global _settings
    if _settings is None:
        # Try to load from config/settings.json first, then environment variables
        settings_file = Path("config/settings.json").absolute()
        if settings_file.exists():
            _settings = Settings.from_json_file(settings_file)
        else:
            # Fall back to environment variables
            _settings = Settings()
    return _settings


def initialize_settings() -> Settings:
    """Initialize settings on application startup."""
    return get_settings()
