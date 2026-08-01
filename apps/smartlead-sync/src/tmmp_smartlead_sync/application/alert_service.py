"""Alert Dispatcher Application Service."""

from __future__ import annotations

from tmmp_integrations_shared.logging import get_logger
from tmmp_smartlead_sync.domain.events import WarmupEvent
from tmmp_smartlead_sync.infrastructure.mattermost_adapter import MattermostAlertAdapter

LOGGER = get_logger(__name__)


class AlertDispatcher:
    """Application service routing Domain Events to Mattermost Notification Adapters."""

    def __init__(self, mattermost_adapter: MattermostAlertAdapter) -> None:
        self._mattermost_adapter = mattermost_adapter

    async def handle_event(self, event: WarmupEvent) -> None:
        LOGGER.info(
            "Handling domain event for account %s: %s",
            event.account_id,
            type(event).__name__,
        )
        res = await self._mattermost_adapter.dispatch_event_notification(event)
        if res.is_fail:
            LOGGER.error("Failed to dispatch Mattermost notification: %s", res.error())
