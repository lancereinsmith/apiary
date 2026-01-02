# Built-in Endpoints

Apiary includes several built-in endpoints for health checks, metrics, authentication, and endpoint discovery.

## Health Check Endpoints

### Basic Health Check

**Endpoint:** `GET /health`

Simple health check that returns the service status.

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### Liveness Probe

**Endpoint:** `GET /health/live`

Kubernetes-compatible liveness probe. Returns 200 if the application is running.

```bash
curl http://localhost:8000/health/live
```

Response:

```json
{
  "status": "alive"
}
```

### Readiness Probe

**Endpoint:** `GET /health/ready`

Kubernetes-compatible readiness probe. Checks if the application and its dependencies are ready to serve traffic.

```bash
curl http://localhost:8000/health/ready
```

Response (healthy):

```json
{
  "status": "ready",
  "dependencies": {
    "external_apis": "healthy"
  },
  "uptime_seconds": 3600
}
```

Response (degraded):

```json
{
  "status": "degraded",
  "dependencies": {
    "external_apis": "unhealthy"
  },
  "uptime_seconds": 3600
}
```

## Metrics Endpoint

**Endpoint:** `GET /metrics`

Returns application metrics including request counts, error rates, and endpoint statistics.

```bash
curl http://localhost:8000/metrics
```

Response:

```json
{
  "total_requests": 1234,
  "total_errors": 5,
  "error_rate": 0.004,
  "endpoints": {
    "/api/crypto": {
      "count": 456,
      "avg_duration_ms": 123.45,
      "errors": 2
    }
  },
  "uptime_seconds": 86400
}
```

## Authentication Endpoints

### Validate API Key

**Endpoint:** `GET /auth/validate`

Validates an API key without requiring authentication.

```bash
# Without key
curl http://localhost:8000/auth/validate

# With key
curl -H "X-API-Key: your-key" http://localhost:8000/auth/validate
```

Response:

```json
{
  "authenticated": true,
  "valid": true
}
```

### Authentication Status

**Endpoint:** `GET /auth/status`

**Requires authentication**

Returns the current authentication status.

```bash
curl -H "X-API-Key: your-key" http://localhost:8000/auth/status
```

Response:

```json
{
  "authenticated": true,
  "api_key": "your-key"
}
```

## Endpoint Discovery

**Endpoint:** `GET /endpoints`

Lists all configurable endpoints and available services.

```bash
curl http://localhost:8000/endpoints
```

Response:

```json
{
  "endpoints": [
    {
      "path": "/api/crypto",
      "method": "GET",
      "service": "crypto",
      "enabled": true,
      "requires_auth": false,
      "description": "Get cryptocurrency price data"
    }
  ],
  "services": ["crypto", "weather"],
  "total": 1
}
```

## API Documentation

### Swagger UI

**Endpoint:** `GET /docs`

Interactive API documentation with Swagger UI.

Visit: `http://localhost:8000/docs`

### ReDoc

**Endpoint:** `GET /redoc`

Alternative API documentation with ReDoc.

Visit: `http://localhost:8000/redoc`

### OpenAPI JSON

**Endpoint:** `GET /openapi.json`

Raw OpenAPI specification in JSON format.

```bash
curl http://localhost:8000/openapi.json
```

## Landing Page

**Endpoint:** `GET /`

HTML landing page (if enabled in settings).

Visit: `http://localhost:8000/`

Can be disabled in `settings.json`:

```json
{
  "enable_landing_page": false
}
```

## Rate Limiting Headers

All endpoints include rate limiting headers:

```text
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1234567890
```

## Using Built-in Endpoints

### Health Checks in Kubernetes

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
```

### Monitoring with Prometheus

Configure Prometheus to scrape `/metrics`:

```yaml
scrape_configs:
  - job_name: 'apiary'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### CI/CD Health Checks

```bash
#!/bin/bash
# Wait for service to be ready
until curl -f http://localhost:8000/health/ready; do
  echo "Waiting for service..."
  sleep 5
done
echo "Service is ready!"
```

## Next Steps

- [Configuration](../getting-started/configuration.md) - Configure endpoints
- [Monitoring](../deployment/monitoring.md) - Set up monitoring
- [Deployment](../deployment/overview.md) - Deploy to production

