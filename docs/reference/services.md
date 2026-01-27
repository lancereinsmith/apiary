# Services Reference

Reference for built-in services.

## Built-in Services

All services inherit from `BaseService` (see [Core Reference](core.md#base-service) for details).

### Hello Service

Simple demonstration service that returns a greeting message.

::: services.hello_service.HelloService
    options:
      show_root_heading: true
      show_source: true

### Crypto Service

Get cryptocurrency price data.

::: services.crypto_service.CryptoService
    options:
      show_root_heading: true
      show_source: true

## Creating Custom Services

See the [Creating Services Guide](../guide/creating-services.md) for detailed information on creating your own services.

**Quick example:**

```python
from core.services.base import BaseService

class MyService(BaseService):
    """My custom service."""

    async def call(self, parameters: dict | None = None) -> dict:
        """Process the service request.

        Args:
            parameters: Optional parameters for the service

        Returns:
            Service response data
        """
        return {"result": "data"}
```

---

## Next Steps

- [Core Reference](core.md)
- [Creating Services Guide](../guide/creating-services.md)
- [Adding Endpoints](../guide/adding-endpoints.md)
