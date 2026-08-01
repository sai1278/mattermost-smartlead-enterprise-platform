"""Prometheus Metrics Collector."""

from __future__ import annotations

from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "integration_http_requests_total",
    "Total HTTP requests executed",
    ["service", "method", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "integration_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["service", "method"],
)


class MetricsCollector:
    """Metrics collector helper for HTTP integrations."""

    def __init__(self, service_name: str) -> None:
        self.service_name = service_name

    def record_request(self, method: str, status_code: int, duration_seconds: float) -> None:
        REQUEST_COUNT.labels(
            service=self.service_name,
            method=method.upper(),
            status_code=str(status_code),
        ).inc()
        REQUEST_LATENCY.labels(
            service=self.service_name,
            method=method.upper(),
        ).observe(duration_seconds)
