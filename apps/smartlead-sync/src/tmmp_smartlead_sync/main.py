"""FastAPI Microservice Application Entrypoint."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import SecretStr
from tmmp_integrations_mattermost import MattermostClient, MattermostConfig
from tmmp_integrations_smartlead import SmartleadClient, SmartleadConfig

from tmmp_smartlead_sync.api.webhook_router import router as webhook_router
from tmmp_smartlead_sync.api.webhook_router import set_webhook_processor
from tmmp_smartlead_sync.application.alert_service import AlertDispatcher
from tmmp_smartlead_sync.application.poll_scheduler import PollingScheduler
from tmmp_smartlead_sync.application.warmup_service import WarmupSyncService
from tmmp_smartlead_sync.application.webhook_processor import SmartleadWebhookProcessor
from tmmp_smartlead_sync.config import SyncWorkerConfig
from tmmp_smartlead_sync.infrastructure.in_memory_repository import InMemoryWarmupRepository
from tmmp_smartlead_sync.infrastructure.mattermost_adapter import MattermostAlertAdapter
from tmmp_smartlead_sync.infrastructure.smartlead_adapter import SmartleadAdapter


def create_app(config: SyncWorkerConfig | None = None) -> FastAPI:
    cfg = config or SyncWorkerConfig()

    smartlead_cfg = SmartleadConfig(
        smartlead_api_url="https://server.smartlead.ai/api/v1",
        api_key=SecretStr("mock-key"),
    )
    smartlead_client = SmartleadClient(smartlead_cfg)
    smartlead_adapter = SmartleadAdapter(smartlead_client)

    mattermost_cfg = MattermostConfig(
        mattermost_url="http://localhost:8065",
        bot_token=SecretStr("mock-bot-token"),
    )
    mattermost_client = MattermostClient(mattermost_cfg)
    mattermost_adapter = MattermostAlertAdapter(mattermost_client, cfg.alert_channel_id)

    repository = InMemoryWarmupRepository()
    alert_dispatcher = AlertDispatcher(mattermost_adapter)
    warmup_service = WarmupSyncService(smartlead_adapter, repository, alert_dispatcher)
    scheduler = PollingScheduler(warmup_service, interval_seconds=cfg.sync_interval_seconds)

    webhook_processor = SmartleadWebhookProcessor(
        alert_dispatcher, cfg.webhook_secret.get_secret_value()
    )
    set_webhook_processor(webhook_processor)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        await scheduler.start()
        yield
        await scheduler.stop()

    app = FastAPI(
        title="Smartlead Sync Worker Microservice",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(webhook_router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "UP", "service": "smartlead-sync"}

    return app


app = create_app()
