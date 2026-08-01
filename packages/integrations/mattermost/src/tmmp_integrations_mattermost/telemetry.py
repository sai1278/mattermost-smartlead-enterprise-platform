"""Mattermost SDK Telemetry Instrumentation."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from opentelemetry.trace import Span, Tracer
from tmmp_integrations_shared.telemetry import (
    get_tracer as shared_get_tracer,
)
from tmmp_integrations_shared.telemetry import (
    trace_span as shared_trace_span,
)


def get_mattermost_tracer() -> Tracer:
    return shared_get_tracer("tmmp-integrations-mattermost")


@asynccontextmanager
async def mattermost_span(
    name: str,
    attributes: dict[str, str] | None = None,
) -> AsyncGenerator[Span, None]:
    tracer = get_mattermost_tracer()
    async with shared_trace_span(tracer, f"mattermost.{name}", attributes=attributes) as span:
        yield span
