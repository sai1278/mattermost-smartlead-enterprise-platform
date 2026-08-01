"""OpenTelemetry Instrumentation Helpers."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from opentelemetry import trace
from opentelemetry.trace import Span, Tracer

from tmmp_integrations_shared.context import get_correlation_id


def get_tracer(service_name: str) -> Tracer:
    """Get OpenTelemetry tracer for service."""
    return trace.get_tracer(service_name)


@asynccontextmanager
async def trace_span(
    tracer: Tracer,
    name: str,
    attributes: dict[str, str] | None = None,
) -> AsyncGenerator[Span, None]:
    """Async context manager to trace execution blocks."""
    attrs = attributes or {}
    attrs["correlation_id"] = get_correlation_id()
    with tracer.start_as_current_span(name) as span:
        for k, v in attrs.items():
            span.set_attribute(k, v)
        yield span
