# Code Quality

Maintain high code quality in Apiary.

## Quick Commands

```bash
black .              # Format code
ruff check .         # Lint
ruff check --fix .   # Auto-fix lint issues
mypy .               # Type check
pytest --cov         # Test with coverage
```

## Code Standards

### Type Hints

Always use type hints:

```python
async def process_data(data: dict[str, Any]) -> dict[str, str]:
    """Process data and return result."""
    return {"status": "success"}
```

### Docstrings

Document public APIs:

```python
def calculate_rate_limit(requests: int, window: int) -> float:
    """Calculate rate limit per second.

    Args:
        requests: Number of allowed requests
        window: Time window in seconds

    Returns:
        Requests per second as float
    """
    return requests / window
```

### Apiary Patterns

Follow existing patterns:

- Services inherit from `BaseService`
- Use dependency injection for HTTP clients and settings
- Raise `APIException` for business logic errors
- Use structured logging with correlation IDs
- Return Pydantic models or dicts from endpoints

### Error Handling

```python
from core.exceptions import APIException

def validate_input(value: str) -> str:
    """Validate input value."""
    if not value:
        raise APIException(
            status_code=400,
            error="INVALID_INPUT",
            message="Value cannot be empty"
        )
    return value
```

## Configuration

Tool configurations are in `pyproject.toml`:

- **Black**: Line length 100, Python 3.11+
- **Ruff**: Selected rules for modern Python
- **Mypy**: Strict mode enabled
- **Pytest**: Coverage reporting configured

## Pre-commit Checks

Optional pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Best Practices

1. **Format before committing** - Always run `black .`
2. **Fix linter warnings** - Run `ruff check --fix .`
3. **Add type hints** - All function signatures
4. **Write tests** - Maintain >80% coverage
5. **Document public APIs** - Clear docstrings
6. **Follow patterns** - Match existing code style
