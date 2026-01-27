# Monitoring

Monitor your Apiary API in production.

## Enable

Edit `config/settings.json` to enable the health router for Kubernetes/Docker deployments:

```json
## config/settings.json

{
  "enabled_routers": ["health"]
}
```

## Health Checks

```bash

## Basic health

curl <https://yourdomain.com/health>

## Readiness check

curl <https://yourdomain.com/health/ready>
```

## Metrics

```bash

## Application metrics

curl <https://yourdomain.com/metrics>
```

## Logs

```bash

## Service logs

sudo journalctl -u apiary -f

## nginx logs

sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Kubernetes Health Probes

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

## Prometheus Integration

Configure Prometheus to scrape `/metrics`:

```yaml
scrape_configs:

- job_name: 'apiary'
    static_configs:
      - targets: ['localhost:8000']

    metrics_path: '/metrics'
```

## Next Steps

- [Configuration](configuration.md) - Production settings
- [Updating](updating.md) - Update workflow and strategies
- [Server Setup](server-setup.md) - Initial setup
