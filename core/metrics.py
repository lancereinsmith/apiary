"""Metrics collection for monitoring."""

import time
from collections import defaultdict
from dataclasses import dataclass, field

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


@dataclass
class EndpointMetrics:
    """Metrics for a single endpoint."""

    count: int = 0
    total_time: float = 0.0
    error_count: int = 0
    last_request_time: float = 0.0
    status_codes: dict[int, int] = field(default_factory=lambda: defaultdict(int))

    @property
    def average_time(self) -> float:
        """Calculate average request time."""
        if self.count == 0:
            return 0.0
        return self.total_time / self.count

    @property
    def error_rate(self) -> float:
        """Calculate error rate."""
        if self.count == 0:
            return 0.0
        return self.error_count / self.count


class MetricsCollector:
    """Collects metrics for the API."""

    def __init__(self):
        """Initialize metrics collector."""
        self._endpoint_metrics: dict[str, EndpointMetrics] = defaultdict(
            EndpointMetrics
        )
        self._start_time = time.time()
        self._total_requests = 0
        self._total_errors = 0

    def record_request(
        self,
        path: str,
        method: str,
        status_code: int,
        duration: float,
    ):
        """Record a request metric.

        Args:
            path: Request path
            method: HTTP method
            status_code: Response status code
            duration: Request duration in seconds
        """
        endpoint_key = f"{method} {path}"
        metrics = self._endpoint_metrics[endpoint_key]

        metrics.count += 1
        metrics.total_time += duration
        metrics.last_request_time = time.time()
        metrics.status_codes[status_code] += 1

        if status_code >= 400:
            metrics.error_count += 1
            self._total_errors += 1

        self._total_requests += 1

    def get_metrics(self) -> dict:
        """Get all collected metrics.

        Returns:
            Dictionary with metrics data
        """
        uptime = time.time() - self._start_time

        endpoint_data = {}
        for endpoint, metrics in self._endpoint_metrics.items():
            endpoint_data[endpoint] = {
                "count": metrics.count,
                "average_time": round(metrics.average_time, 4),
                "error_count": metrics.error_count,
                "error_rate": round(metrics.error_rate, 4),
                "status_codes": dict(metrics.status_codes),
            }

        return {
            "uptime_seconds": round(uptime, 2),
            "total_requests": self._total_requests,
            "total_errors": self._total_errors,
            "error_rate": (
                round(self._total_errors / self._total_requests, 4)
                if self._total_requests > 0
                else 0.0
            ),
            "endpoints": endpoint_data,
        }

    def reset(self):
        """Reset all metrics."""
        self._endpoint_metrics.clear()
        self._start_time = time.time()
        self._total_requests = 0
        self._total_errors = 0


# Global metrics collector instance
metrics_collector = MetricsCollector()


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting metrics."""

    async def dispatch(self, request: Request, call_next):
        """Collect metrics for requests."""
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        # Record metrics
        metrics_collector.record_request(
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            duration=duration,
        )

        return response
