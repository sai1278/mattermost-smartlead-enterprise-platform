"""Smartlead Webhook Payload Deserialization and Signature Verification."""

from __future__ import annotations

import hashlib
import hmac
from typing import Any

from pydantic import Field
from tmmp_integrations_shared.dto import BaseDTO

from tmmp_integrations_smartlead.errors import SmartleadWebhookValidationError
from tmmp_integrations_smartlead.models import WebhookEventType


class SmartleadWebhookPayload(BaseDTO):
    event_type: WebhookEventType
    event_id: str
    timestamp: str
    account_id: int
    data: dict[str, Any] = Field(default_factory=dict)


class SmartleadWebhookValidator:
    """HMAC SHA256 Webhook Validator."""

    @staticmethod
    def validate_signature(
        payload_bytes: bytes,
        signature: str,
        secret: str,
    ) -> bool:
        """Verify HMAC SHA256 signature against secret."""
        if not signature or not secret:
            return False
        expected_sig = hmac.new(
            secret.encode("utf-8"),
            payload_bytes,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected_sig, signature)

    @staticmethod
    def parse_event(raw_json: dict[str, Any]) -> SmartleadWebhookPayload:
        """Parse raw json dictionary into typed SmartleadWebhookPayload."""
        try:
            return SmartleadWebhookPayload.model_validate(raw_json)
        except Exception as exc:
            raise SmartleadWebhookValidationError(
                f"Failed to parse webhook payload: {exc}"
            ) from exc
