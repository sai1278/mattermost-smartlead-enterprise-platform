"""Mapper converting domain entities to ClickHouse columnar formats."""

from __future__ import annotations

from typing import Any

from tmmp_analytics.domain.models import AlertHistory, WarmupMetrics


class MetricsMapper:
    """Maps domain metric entities to list rows for ClickHouse insertion."""

    @staticmethod
    def map_warmup_metrics(metric: WarmupMetrics) -> list[Any]:
        return [
            metric.mailbox,
            metric.timestamp.isoformat(),
            metric.total_sent,
            metric.total_inbox,
            metric.total_spam,
            metric.total_replies,
        ]

    @staticmethod
    def map_alert_history(alert: AlertHistory) -> list[Any]:
        return [
            alert.alert_id,
            alert.timestamp.isoformat(),
            alert.account_email,
            alert.severity,
            alert.message,
        ]
