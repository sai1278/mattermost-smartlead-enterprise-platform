"""FastAPI Mattermost Bot Microservice Entrypoint."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tmmp_integrations_mattermost import MattermostClient, MattermostConfig

from tmmp_mattermost_bot.application.bot_service import MattermostBotService
from tmmp_mattermost_bot.application.event_dispatcher import BotEventDispatcher
from tmmp_mattermost_bot.config import BotConfig
from tmmp_mattermost_bot.infrastructure.mattermost_rest_adapter import MattermostBotRESTAdapter
from tmmp_mattermost_bot.infrastructure.mattermost_ws_adapter import MattermostWebSocketAdapter


def create_app(config: BotConfig | None = None) -> FastAPI:
    cfg = config or BotConfig()

    mattermost_cfg = MattermostConfig(
        mattermost_url=cfg.mattermost_url,
        bot_token=cfg.bot_token,
    )
    mattermost_client = MattermostClient(mattermost_cfg)
    rest_adapter = MattermostBotRESTAdapter(mattermost_client)
    ws_adapter = MattermostWebSocketAdapter(
        ws_url=cfg.ws_url,
        bot_token=cfg.bot_token.get_secret_value(),
    )

    event_dispatcher = BotEventDispatcher(rest_adapter, cfg.bot_username)
    bot_service = MattermostBotService(ws_adapter, event_dispatcher)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        await bot_service.start()
        yield
        await bot_service.stop()

    app = FastAPI(
        title="Mattermost WebSocket Bot Microservice",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        status_str = "UP" if bot_service.is_connected else "DOWN"
        return {"status": status_str, "service": "mattermost-bot"}

    return app


app = create_app()
