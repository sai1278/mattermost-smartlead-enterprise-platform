import asyncio

from tmmp_integrations_shared.flags import InMemoryFeatureFlagProvider
from tmmp_integrations_shared.health import HealthCheckResult, HealthStatus


def test_health_check_result():
    res = HealthCheckResult(
        service="test-service",
        status=HealthStatus.HEALTHY,
        details={"db": "up"},
    )
    assert res.service == "test-service"
    assert res.status == HealthStatus.HEALTHY


def test_feature_flags():
    async def _test():
        provider = InMemoryFeatureFlagProvider({"new_ui": True})
        assert await provider.is_enabled("new_ui") is True
        assert await provider.is_enabled("unknown", default=False) is False
        provider.set_flag("unknown", True)
        assert await provider.is_enabled("unknown") is True

    asyncio.run(_test())
