"""Smartlead Service Health Check."""

from __future__ import annotations

from tmmp_integrations_shared.health import HealthCheckableProtocol, HealthCheckResult, HealthStatus

from tmmp_integrations_smartlead.client import SmartleadClient


class SmartleadHealthCheck(HealthCheckableProtocol):
    """Health check implementation querying Smartlead API campaigns ping."""

    def __init__(self, client: SmartleadClient) -> None:
        self._client = client

    async def check_health(self) -> HealthCheckResult:
        res = await self._client.ping()
        if res.is_ok:
            return HealthCheckResult(
                service="smartlead-api",
                status=HealthStatus.HEALTHY,
                details={"status": "UP"},
            )
        return HealthCheckResult(
            service="smartlead-api",
            status=HealthStatus.UNHEALTHY,
            details={"error": str(res.error())},
        )
