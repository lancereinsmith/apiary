# Testing

Write and run tests for Apiary.

## Running Tests

```bash
pytest                   # All tests
pytest --cov             # With coverage
pytest -v                # Verbose
pytest tests/unit/       # Unit tests only
pytest tests/integration/ # Integration tests only
pytest -x                # Stop at first failure
```

## Test Structure

```text
tests/
├── conftest.py          # Shared fixtures
├── unit/                # Unit tests
│   ├── test_services.py # Service tests
│   └── test_auth.py     # Auth tests
└── integration/         # Integration tests
    └── test_endpoints.py # Endpoint tests
```

## Available Fixtures

From `conftest.py`:

- `client` - TestClient for sync requests
- `async_client` - AsyncClient for async tests
- `mock_settings` - Mock settings object
- `mock_http_client` - Mock HTTP client
- `auth_headers` - Valid auth headers dict
- `no_auth_headers` - Empty headers dict

## Writing Tests

### Unit Test for Services

```python
import pytest
from services.crypto_service import CryptoService

@pytest.mark.asyncio
async def test_crypto_service(mock_http_client):
    """Test crypto service returns expected data."""
    service = CryptoService(http_client=mock_http_client)
    result = await service.call({"symbol": "BTC"})

    assert result["symbol"] == "BTC"
    assert "price" in result
```

### Integration Test for Endpoints

```python
def test_health_endpoint(client):
    """Test health endpoint returns healthy status."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Testing Authentication

```python
def test_protected_endpoint_no_auth(client, no_auth_headers):
    """Test protected endpoint requires authentication."""
    response = client.get("/api/protected", headers=no_auth_headers)

    assert response.status_code == 401


def test_protected_endpoint_with_auth(client, auth_headers):
    """Test protected endpoint succeeds with valid auth."""
    response = client.get("/api/protected", headers=auth_headers)

    assert response.status_code == 200
```

### Testing Configurable Endpoints

```python
def test_configurable_endpoint(client):
    """Test dynamically created endpoint."""
    response = client.get("/api/crypto")

    assert response.status_code == 200
    assert "symbol" in response.json()
```

## Testing New Services

When creating a new service, test:

1. **Success case** - Valid input returns expected output
2. **Error handling** - Invalid input raises appropriate errors
3. **Edge cases** - Empty params, missing fields, etc.
4. **HTTP calls** - Mock external API calls

Example:

```python
@pytest.mark.asyncio
async def test_weather_service_success(mock_http_client):
    """Test weather service with valid input."""
    service = WeatherService(http_client=mock_http_client)
    result = await service.call({"city": "Boston"})

    assert result["city"] == "Boston"
    assert "temperature" in result


@pytest.mark.asyncio
async def test_weather_service_missing_city(mock_http_client):
    """Test weather service handles missing city."""
    service = WeatherService(http_client=mock_http_client)

    with pytest.raises(APIException) as exc:
        await service.call({})

    assert exc.value.status_code == 400
```

## Coverage

Maintain >80% coverage:

```bash
pytest --cov --cov-report=html
open htmlcov/index.html  # View coverage report
```

## Next Steps

- [Code Quality](code-quality.md) - Maintain quality standards
- [Development Setup](setup.md) - Set up dev environment
