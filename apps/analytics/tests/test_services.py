import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from tmmp_analytics.application.services import (
    AnalyticsIngestionService,
    MetricsAggregationService,
)
from tmmp_analytics.domain.models import DailyMetrics, WarmupMetrics
from tmmp_integrations_shared.dto import Result


def test_analytics_services():
    repo = MagicMock()
    repo.save_warmup_metric = AsyncMock()
    dummy_summary = DailyMetrics("2026-08-01", 100, 90, 10, 90.0)
    repo.get_daily_summary = AsyncMock(return_value=Result.ok(dummy_summary))

    ingest_svc = AnalyticsIngestionService(repo)
    agg_svc = MetricsAggregationService(repo)

    metric = WarmupMetrics("a@b.com", datetime.utcnow(), 10, 9, 1, 2)

    async def _test():
        await ingest_svc.ingest_metric(metric)
        assert repo.save_warmup_metric.called

        res = await agg_svc.get_daily_summary()
        assert res.is_ok
        assert res.unwrap().total_sent == 100

    asyncio.run(_test())
