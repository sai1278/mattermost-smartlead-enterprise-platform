from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient
from tmmp_analytics.api.router import set_services
from tmmp_analytics.domain.models import DailyMetrics
from tmmp_analytics.main import create_app
from tmmp_integrations_shared.dto import Result


def test_analytics_health_endpoint():
    app = create_app()
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "enterprise-analytics"


def test_analytics_daily_summary_endpoint():
    ingest_svc = MagicMock()
    agg_svc = MagicMock()
    trend_svc = MagicMock()

    dummy_summary = DailyMetrics("2026-08-01", 1500, 1450, 50, 96.67)
    agg_svc.get_daily_summary = AsyncMock(return_value=Result.ok(dummy_summary))

    set_services(ingest_svc, agg_svc, trend_svc)

    app = create_app()
    set_services(ingest_svc, agg_svc, trend_svc)

    client = TestClient(app)
    response = client.get("/analytics/daily-summary")
    assert response.status_code == 200
    assert response.json()["date"] == "2026-08-01"
    assert response.json()["total_sent"] == 1500
