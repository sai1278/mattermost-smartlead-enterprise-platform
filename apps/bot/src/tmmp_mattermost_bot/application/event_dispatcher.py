"""Bot Event Dispatcher Application Service."""

from __future__ import annotations

import json

from tmmp_integrations_mattermost import MattermostWebSocketEvent
from tmmp_integrations_shared.logging import get_logger
from tmmp_mattermost_bot.infrastructure.mattermost_rest_adapter import MattermostBotRESTAdapter

LOGGER = get_logger(__name__)


class BotEventDispatcher:
    """Dispatches raw WebSocket events to appropriate Bot Handlers."""

    def __init__(self, rest_adapter: MattermostBotRESTAdapter, bot_username: str) -> None:
        self._rest = rest_adapter
        self._bot_username = bot_username.lstrip("@")

    async def dispatch_ws_event(self, event: MattermostWebSocketEvent) -> None:
        if event.event != "posted":
            return

        raw_post_str = event.data.get("post", "{}")
        try:
            post_data = json.loads(raw_post_str)
        except Exception:
            return

        message = str(post_data.get("message", ""))
        channel_id = str(post_data.get("channel_id", ""))
        post_id = str(post_data.get("id", ""))

        if f"@{self._bot_username}" in message:
            LOGGER.info("Bot mentioned in post %s channel %s", post_id, channel_id)
            reply_text = (
                f"Hello! I am @{self._bot_username}. How can I assist with your Smartlead Warmup?"
            )
            await self._rest.post_reply(channel_id=channel_id, root_id=post_id, message=reply_text)
