"""Health Check Abstractions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


class HealthStatus(Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"


@dataclass(frozen=True)
class HealthCheckResult:
    service: str
    status: HealthStatus
    details: dict[str, Any]


class HealthCheckableProtocol(Protocol):
    """Protocol for services supporting health checks."""

    async def check_health(self) -> HealthCheckResult: ...
