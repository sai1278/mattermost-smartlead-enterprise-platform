"""Analytics Microservice Package."""

from tmmp_analytics.config import AnalyticsConfig
from tmmp_analytics.domain.models import DailyMetrics, MailboxTrend, WarmupMetrics

__all__ = [
    "AnalyticsConfig",
    "DailyMetrics",
    "MailboxTrend",
    "WarmupMetrics",
]
