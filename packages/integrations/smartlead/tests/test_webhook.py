import hashlib
import hmac

import pytest
from tmmp_integrations_smartlead.errors import SmartleadWebhookValidationError
from tmmp_integrations_smartlead.models import WebhookEventType
from tmmp_integrations_smartlead.webhook import SmartleadWebhookValidator


def test_webhook_signature_validation():
    secret = "my_webhook_secret_key"
    payload = (
        b'{"event_type": "EMAIL_SENT", "event_id": "evt_1", '
        b'"timestamp": "2026-07-30T12:00:00Z", "account_id": 101}'
    )
    signature = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()

    valid = SmartleadWebhookValidator.validate_signature(payload, signature, secret)
    assert valid is True

    invalid = SmartleadWebhookValidator.validate_signature(payload, "bad_sig", secret)
    assert invalid is False


def test_webhook_parsing():
    data = {
        "event_type": "EMAIL_SENT",
        "event_id": "evt_1",
        "timestamp": "2026-07-30T12:00:00Z",
        "account_id": 101,
        "data": {"recipient": "prospect@target.com"},
    }
    event = SmartleadWebhookValidator.parse_event(data)
    assert event.event_type == WebhookEventType.EMAIL_SENT
    assert event.account_id == 101
    assert event.data["recipient"] == "prospect@target.com"


def test_invalid_webhook_parsing():
    with pytest.raises(SmartleadWebhookValidationError):
        SmartleadWebhookValidator.parse_event({"bad_key": "val"})
