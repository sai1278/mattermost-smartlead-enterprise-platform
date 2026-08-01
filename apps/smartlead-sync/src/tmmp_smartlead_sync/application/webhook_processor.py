"""Smartlead Webhook Event Processor."""

from __future__ import annotations

from typing import Any

from tmmp_integrations_shared.logging import get_logger
from tmmp_integrations_smartlead.webhook import SmartleadWebhookPayload, SmartleadWebhookValidator
from tmmp_smartlead_sync.application.alert_service import AlertDispatcher
from tmmp_smartlead_sync.domain.events import WarmupWarning

LOGGER = get_logger(__name__)


class SmartleadWebhookProcessor:
    """Processes incoming validated webhooks and triggers application handlers."""

    def __init__(self, alert_dispatcher: AlertDispatcher, secret: str) -> None:
        self._alert = alert_dispatcher
        self._secret = secret

    async def process_webhook(
        self, raw_body: bytes, signature: str, raw_json: dict[str, Any]
    ) -> bool:
        if self._secret and not SmartleadWebhookValidator.validate_signature(
            raw_body, signature, self._secret
        ):
            LOGGER.error("Invalid webhook signature received.")
            return False

        payload: SmartleadWebhookPayload = SmartleadWebhookValidator.parse_event(raw_json)
        LOGGER.info("Received valid Smartlead webhook event: %s", payload.event_type)

        if payload.event_type.value == "WARMUP_PAUSED":
            event = WarmupWarning(
                account_id=payload.account_id,
                email=str(payload.data.get("email", f"acc-{payload.account_id}")),
                reason="Warmup automatically paused by Smartlead.",
            )
            await self._alert.handle_event(event)

        return True
