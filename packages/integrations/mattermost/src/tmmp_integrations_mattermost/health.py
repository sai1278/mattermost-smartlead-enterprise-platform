"""Mattermost Service Health Check."""

from __future__ import annotations

from tmmp_integrations_shared.health import HealthCheckableProtocol, HealthCheckResult, HealthStatus

from tmmp_integrations_mattermost.client import MattermostClient


class MattermostHealthCheck(HealthCheckableProtocol):
    """Health check implementation querying Mattermost system ping endpoint."""

    def __init__(self, client: MattermostClient) -> None:
        self._client = client

    async def check_health(self) -> HealthCheckResult:
        res = await self._client.ping()
        if res.is_ok and res.unwrap().get("status") == "OK":
            return HealthCheckResult(
                service="mattermost-api",
                status=HealthStatus.HEALTHY,
                details={"ping": "OK"},
            )
        return HealthCheckResult(
            service="mattermost-api",
            status=HealthStatus.UNHEALTHY,
            details={"error": str(res.error())},
        )
