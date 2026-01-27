# Models Reference

Reference for request and response models used throughout Apiary.

## Response Models

::: models.responses
    options:
      show_root_heading: true
      show_source: true

## Request Models

::: models.requests
    options:
      show_root_heading: true
      show_source: true

## Usage Examples

### Using Response Models

```python
from models.responses import BaseResponse

class MyResponse(BaseResponse):
    """Custom response model."""
    data: dict
    count: int

# All responses automatically include timestamp
response = MyResponse(data={"key": "value"}, count=1)
```

### Using Request Models

```python
from pydantic import BaseModel

class QueryParams(BaseModel):
    """Query parameters for endpoint."""
    name: str
    limit: int = 10

@router.get("/items")
async def get_items(params: QueryParams = Depends()):
    return {"items": []}
```

---

## Next Steps

- [Core Reference](core.md)
- [Services Reference](services.md)
- [Adding Endpoints](../guide/adding-endpoints.md)
