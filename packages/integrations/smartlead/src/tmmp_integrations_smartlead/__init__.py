"""Smartlead Integration SDK Package Public API."""

from tmmp_integrations_smartlead.auth import SmartleadAuth
from tmmp_integrations_smartlead.client import SmartleadClient
from tmmp_integrations_smartlead.config import SmartleadConfig
from tmmp_integrations_smartlead.dto import (
    Campaign,
    DailyWarmupMetrics,
    EmailAccount,
    ReputationMetrics,
    WarmupAccount,
    WarmupStats,
)
from tmmp_integrations_smartlead.endpoints import Routes
from tmmp_integrations_smartlead.errors import (
    SmartleadAPIError,
    SmartleadAuthError,
    SmartleadSDKError,
    SmartleadWebhookValidationError,
)
from tmmp_integrations_smartlead.health import SmartleadHealthCheck
from tmmp_integrations_smartlead.models import (
    CampaignStatus,
    MailboxHealth,
    WarmupStage,
    WebhookEventType,
)
from tmmp_integrations_smartlead.pagination import SmartleadPaginator
from tmmp_integrations_smartlead.webhook import SmartleadWebhookPayload, SmartleadWebhookValidator

__all__ = [
    "Campaign",
    "CampaignStatus",
    "DailyWarmupMetrics",
    "EmailAccount",
    "MailboxHealth",
    "ReputationMetrics",
    "Routes",
    "SmartleadAPIError",
    "SmartleadAuth",
    "SmartleadAuthError",
    "SmartleadClient",
    "SmartleadConfig",
    "SmartleadHealthCheck",
    "SmartleadPaginator",
    "SmartleadSDKError",
    "SmartleadWebhookPayload",
    "SmartleadWebhookValidationError",
    "SmartleadWebhookValidator",
    "WarmupAccount",
    "WarmupStage",
    "WarmupStats",
    "WebhookEventType",
]
