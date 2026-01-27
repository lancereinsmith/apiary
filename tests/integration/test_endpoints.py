"""Integration tests for API endpoints."""


def test_home_endpoint(client):
    """Test home page endpoint."""
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_health_live_endpoint(client):
    """Test liveness probe endpoint."""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


def test_health_ready_endpoint(client):
    """Test readiness probe endpoint."""
    # This endpoint makes real HTTP calls, so it may fail in tests
    # We'll just check that it returns a response (even if degraded)
    response = client.get("/health/ready")
    # Accept both 200 (ready) and 503 (degraded/unready) as valid responses
    assert response.status_code in [200, 503]
    if response.status_code == 200:
        data = response.json()
        assert "status" in data
        assert "dependencies" in data
        assert "uptime_seconds" in data


def test_endpoints_discovery(client):
    """Test endpoint discovery endpoint."""
    response = client.get("/endpoints")
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data
    assert "services" in data
    assert "total" in data
    assert isinstance(data["endpoints"], list)
    assert isinstance(data["services"], list)


def test_auth_validate_no_key(client):
    """Test auth validate endpoint without API key."""
    response = client.get("/auth/validate")
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is False


def test_auth_validate_invalid_key(client):
    """Test auth validate endpoint with invalid API key."""
    response = client.get("/auth/validate", headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is False


def test_auth_status_no_key(client):
    """Test auth status endpoint without API key."""
    response = client.get("/auth/status")
    assert response.status_code == 401


def test_favicon_endpoint(client):
    """Test favicon endpoint."""
    response = client.get("/favicon.ico", follow_redirects=False)
    assert response.status_code in [200, 302, 307]  # May redirect or serve directly
