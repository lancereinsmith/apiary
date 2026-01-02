# Models Reference

Reference for request and response models.

## Response Models

### BaseResponse

```python
from models.responses import BaseResponse

class MyResponse(BaseResponse):
    data: dict
    count: int
```

All responses include:

- `timestamp`: ISO 8601 timestamp

## Request Models

### Query Parameters

```python
from pydantic import BaseModel

class QueryParams(BaseModel):
    name: str
    limit: int = 10
```

## Next Steps

- [Core Reference](core.md)
- [Services Reference](services.md)

