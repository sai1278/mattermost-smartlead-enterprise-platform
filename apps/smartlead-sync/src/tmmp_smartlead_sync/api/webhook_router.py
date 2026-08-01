"""FastAPI APIRouter for Smartlead Webhooks."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Header, HTTPException, Request, status
from tmmp_smartlead_sync.application.webhook_processor import SmartleadWebhookProcessor

router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])

_processor_instance: SmartleadWebhookProcessor | None = None


def set_webhook_processor(processor: SmartleadWebhookProcessor) -> None:
    global _processor_instance
    _processor_instance = processor


@router.post("/smartlead", status_code=status.HTTP_200_OK)
async def handle_smartlead_webhook(
    request: Request,
    x_smartlead_signature: str = Header(default="", alias="X-Smartlead-Signature"),
) -> dict[str, Any]:
    if not _processor_instance:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Webhook processor not initialized",
        )

    raw_body = await request.body()
    raw_json = await request.json()

    success = await _processor_instance.process_webhook(raw_body, x_smartlead_signature, raw_json)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature",
        )

    return {"status": "accepted"}
