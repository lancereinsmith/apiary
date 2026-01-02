# Services Reference

Reference for built-in services.

## Crypto Service

Get cryptocurrency price data.

```python
from services.crypto_service import CryptoService

service = CryptoService()
result = await service.call({"symbol": "BTC"})
```

### Parameters

- `symbol` (optional): Cryptocurrency symbol (BTC, ETH, SOL, etc.)

### Response

```json
{
  "symbol": "BTC",
  "name": "Bitcoin",
  "price_usd": 87555.25,
  "rank": 1,
  "percent_change_24h": -0.22
}
```

## Creating Custom Services

```python
from core.services.base import BaseService

class MyService(BaseService):
    async def call(self, parameters=None):
        return {"result": "data"}
```

## Next Steps

- [Core Reference](core.md)
- [Creating Services Guide](../guide/creating-services.md)

