"""Service modules for business logic."""

# Register services for dynamic endpoint configuration
from core.services import register_service
from services.crypto_service import CryptoService

# Register services
register_service("crypto", CryptoService)
