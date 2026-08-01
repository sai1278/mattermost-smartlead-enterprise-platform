"""Smartlead Adapter wrapping SDK Client."""

from __future__ import annotations

from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError
from tmmp_integrations_smartlead import EmailAccount, SmartleadClient, WarmupStats
from tmmp_smartlead_sync.domain.entities import WarmupMetricsSnapshot


class SmartleadAdapter:
    """Adapter transforming Smartlead SDK payloads into Domain Entities."""

    def __init__(self, client: SmartleadClient) -> None:
        self._client = client

    async def fetch_accounts(self) -> Result[list[EmailAccount], IntegrationError]:
        return await self._client.list_email_accounts()

    async def fetch_metrics_snapshot(
        self, account: EmailAccount
    ) -> Result[WarmupMetricsSnapshot, IntegrationError]:
        stats_res = await self._client.get_warmup_stats(account.id)
        if stats_res.is_fail:
            return Result.fail(stats_res.error() or IntegrationError("Failed to fetch stats"))

        stats: WarmupStats = stats_res.unwrap()
        total_sent = max(1, stats.sent_count)
        bounce_rate = (stats.bounce_count / total_sent) * 100.0

        snapshot = WarmupMetricsSnapshot(
            account_id=account.id,
            email=account.from_email,
            sent_count=stats.sent_count,
            inbox_count=stats.inbox_count,
            spam_count=stats.spam_count,
            bounce_count=stats.bounce_count,
            inbox_rate=stats.inbox_rate,
            spam_rate=stats.spam_rate,
            bounce_rate=bounce_rate,
        )
        return Result.ok(snapshot)
