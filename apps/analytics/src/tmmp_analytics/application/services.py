"""Analytics Application Services."""

from __future__ import annotations

from tmmp_analytics.domain.models import DailyMetrics, MailboxTrend, WarmupMetrics
from tmmp_analytics.infrastructure.clickhouse_repository import ClickHouseRepository
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError
from tmmp_integrations_shared.logging import get_logger

LOGGER = get_logger(__name__)


class AnalyticsIngestionService:
    """Service handling metrics ingestion."""

    def __init__(self, repo: ClickHouseRepository) -> None:
        self._repo = repo

    async def ingest_metric(self, metric: WarmupMetrics) -> None:
        LOGGER.info("Ingesting metric for mailbox %s", metric.mailbox)
        await self._repo.save_warmup_metric(metric)


class MetricsAggregationService:
    """Service aggregating metrics data."""

    def __init__(self, repo: ClickHouseRepository) -> None:
        self._repo = repo

    async def get_daily_summary(self) -> Result[DailyMetrics, IntegrationError]:
        return await self._repo.get_daily_summary()


class TrendCalculationService:
    """Service computing domain deliverability trends."""

    def __init__(self, repo: ClickHouseRepository) -> None:
        self._repo = repo

    async def get_domain_trend(self, domain: str) -> Result[MailboxTrend, IntegrationError]:
        return await self._repo.get_domain_trend(domain)


class RetentionService:
    """Service cleaning up expired analytics partition data."""

    def __init__(self, repo: ClickHouseRepository, retention_days: int = 90) -> None:
        self._repo = repo
        self._retention_days = retention_days

    async def cleanup_old_records(self) -> None:
        LOGGER.info(
            "Executing retention partition cleanup (older than %d days)...",
            self._retention_days,
        )
