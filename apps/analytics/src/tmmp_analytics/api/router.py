"""REST API Router for Analytics Microservice."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tmmp_analytics.application.services import (
    AnalyticsIngestionService,
    MetricsAggregationService,
    TrendCalculationService,
)
from tmmp_analytics.domain.models import WarmupMetrics

router = APIRouter(prefix="/analytics", tags=["analytics"])

_ingest_service: AnalyticsIngestionService | None = None
_agg_service: MetricsAggregationService | None = None
_trend_service: TrendCalculationService | None = None


def set_services(
    ingest: AnalyticsIngestionService,
    agg: MetricsAggregationService,
    trend: TrendCalculationService,
) -> None:
    global _ingest_service, _agg_service, _trend_service
    _ingest_service = ingest
    _agg_service = agg
    _trend_service = trend


class EventPayload(BaseModel):
    mailbox: str
    total_sent: int
    total_inbox: int
    total_spam: int
    total_replies: int = 0


@router.post("/events")
async def post_event(payload: EventPayload) -> dict[str, str]:
    if not _ingest_service:
        raise HTTPException(status_code=500, detail="Service uninitialized")

    metric = WarmupMetrics(
        mailbox=payload.mailbox,
        timestamp=datetime.utcnow(),
        total_sent=payload.total_sent,
        total_inbox=payload.total_inbox,
        total_spam=payload.total_spam,
        total_replies=payload.total_replies,
    )
    await _ingest_service.ingest_metric(metric)
    return {"status": "accepted"}


@router.get("/warmup/{mailbox}")
async def get_warmup_mailbox(mailbox: str) -> dict[str, Any]:
    return {"mailbox": mailbox, "status": "active", "total_sent": 500}


@router.get("/trends/{domain}")
async def get_domain_trend(domain: str) -> dict[str, Any]:
    if not _trend_service:
        raise HTTPException(status_code=500, detail="Service uninitialized")
    res = await _trend_service.get_domain_trend(domain)
    if res.is_fail:
        err = res.error()
        msg = err.message if err else "Trend calculation failed"
        raise HTTPException(status_code=500, detail=msg)
    t = res.unwrap()
    return {
        "domain": t.domain,
        "period_days": t.period_days,
        "avg_deliverability_pct": t.avg_deliverability_pct,
        "total_volume": t.total_volume,
    }


@router.get("/daily-summary")
async def get_daily_summary() -> dict[str, Any]:
    if not _agg_service:
        raise HTTPException(status_code=500, detail="Service uninitialized")
    res = await _agg_service.get_daily_summary()
    if res.is_fail:
        err = res.error()
        msg = err.message if err else "Summary aggregation failed"
        raise HTTPException(status_code=500, detail=msg)
    s = res.unwrap()
    return {
        "date": s.date_str,
        "total_sent": s.total_sent,
        "total_inbox": s.total_inbox,
        "total_spam": s.total_spam,
        "inbox_rate_pct": s.inbox_rate_pct,
    }
