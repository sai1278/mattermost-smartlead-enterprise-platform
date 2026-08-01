"""FastAPI Analytics Microservice Entrypoint."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tmmp_integrations_clickhouse import ClickHouseClient, ClickHouseConfig

from tmmp_analytics.api.router import router, set_services
from tmmp_analytics.application.services import (
    AnalyticsIngestionService,
    MetricsAggregationService,
    TrendCalculationService,
)
from tmmp_analytics.config import AnalyticsConfig
from tmmp_analytics.infrastructure.batch_writer import BatchWriter
from tmmp_analytics.infrastructure.clickhouse_repository import ClickHouseRepository


def create_app(config: AnalyticsConfig | None = None) -> FastAPI:
    cfg = config or AnalyticsConfig()

    ch_client = ClickHouseClient(ClickHouseConfig())
    batch_writer = BatchWriter(
        ch_client,
        batch_size=cfg.batch_size,
        flush_interval=cfg.batch_flush_seconds,
    )
    repo = ClickHouseRepository(ch_client, batch_writer)

    ingest_svc = AnalyticsIngestionService(repo)
    agg_svc = MetricsAggregationService(repo)
    trend_svc = TrendCalculationService(repo)

    set_services(ingest_svc, agg_svc, trend_svc)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        yield
        await batch_writer.flush()
        await ch_client.close()

    app = FastAPI(
        title="Enterprise Analytics Microservice",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "UP", "service": "enterprise-analytics"}

    return app


app = create_app()
