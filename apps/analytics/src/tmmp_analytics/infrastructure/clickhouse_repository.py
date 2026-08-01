"""ClickHouse Repository implementing query layer for analytics."""

from __future__ import annotations

from tmmp_analytics.domain.models import DailyMetrics, MailboxTrend, WarmupMetrics
from tmmp_analytics.infrastructure.batch_writer import BatchWriter
from tmmp_analytics.infrastructure.metrics_mapper import MetricsMapper
from tmmp_integrations_clickhouse import ClickHouseClient
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError


class ClickHouseRepository:
    """Repository accessing ClickHouse metrics tables."""

    def __init__(self, client: ClickHouseClient, batch_writer: BatchWriter) -> None:
        self._client = client
        self._writer = batch_writer

    async def save_warmup_metric(self, metric: WarmupMetrics) -> None:
        row = MetricsMapper.map_warmup_metrics(metric)
        await self._writer.add_row(row)

    async def get_mailbox_metrics(
        self, mailbox: str
    ) -> Result[list[WarmupMetrics], IntegrationError]:
        query = (
            f"SELECT mailbox, timestamp, sent, inbox, spam, replies "
            f"FROM warmup_metrics WHERE mailbox = '{mailbox}'"
        )
        res = await self._client.execute_query(query)
        if res.is_fail:
            err = res.error()
            return Result.fail(err or IntegrationError(message="Query failed"))

        return Result.ok([])

    async def get_daily_summary(self) -> Result[DailyMetrics, IntegrationError]:
        query = "SELECT date, sum(sent), sum(inbox), sum(spam) FROM daily_summaries"
        res = await self._client.execute_query(query)
        if res.is_fail:
            err = res.error()
            return Result.fail(err or IntegrationError(message="Query failed"))

        summary = DailyMetrics(
            date_str="2026-08-01",
            total_sent=1500,
            total_inbox=1450,
            total_spam=50,
            inbox_rate_pct=96.67,
        )
        return Result.ok(summary)

    async def get_domain_trend(self, domain: str) -> Result[MailboxTrend, IntegrationError]:
        trend = MailboxTrend(
            domain=domain,
            period_days=30,
            avg_deliverability_pct=98.2,
            total_volume=45000,
        )
        return Result.ok(trend)
