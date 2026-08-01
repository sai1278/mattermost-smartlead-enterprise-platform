"""FastAPI Command Handler Microservice Entrypoint."""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import SecretStr
from tmmp_integrations_smartlead import SmartleadClient, SmartleadConfig

from tmmp_command_handler.api.command_router import router as command_router
from tmmp_command_handler.api.command_router import set_command_dispatcher
from tmmp_command_handler.application.dispatcher import CommandDispatcher
from tmmp_command_handler.application.warmup_commands import WarmupCommandHandler
from tmmp_command_handler.config import CommandHandlerConfig
from tmmp_command_handler.infrastructure.mattermost_adapter import MattermostResponseAdapter
from tmmp_command_handler.infrastructure.smartlead_adapter import SmartleadCommandAdapter


def create_app(config: CommandHandlerConfig | None = None) -> FastAPI:
    cfg = config or CommandHandlerConfig()

    smartlead_cfg = SmartleadConfig(
        smartlead_api_url="https://server.smartlead.ai/api/v1",
        api_key=SecretStr("mock-key"),
    )
    smartlead_client = SmartleadClient(smartlead_cfg)
    smartlead_adapter = SmartleadCommandAdapter(smartlead_client)
    response_adapter = MattermostResponseAdapter()

    warmup_handler = WarmupCommandHandler(smartlead_adapter, response_adapter)
    dispatcher = CommandDispatcher(warmup_handler)

    set_command_dispatcher(dispatcher, cfg.mattermost_token.get_secret_value())

    app = FastAPI(
        title="Mattermost Slash Command Handler Microservice",
        version="0.1.0",
    )

    app.include_router(command_router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "UP", "service": "command-handler"}

    return app


app = create_app()
