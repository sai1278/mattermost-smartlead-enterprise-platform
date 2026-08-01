import asyncio
from unittest.mock import AsyncMock, MagicMock

from tmmp_integrations_mattermost import MattermostWebSocketEvent
from tmmp_mattermost_bot.application.event_dispatcher import BotEventDispatcher


def test_bot_event_dispatcher_mention():
    rest_adapter = MagicMock()
    rest_adapter.post_reply = AsyncMock()

    dispatcher = BotEventDispatcher(rest_adapter, bot_username="warmupbot")

    post_json = (
        '{"id": "post101", "channel_id": "chan1", "message": "Hey @warmupbot please check status"}'
    )
    ws_event = MattermostWebSocketEvent(
        {
            "event": "posted",
            "data": {"post": post_json},
        }
    )

    async def _test():
        await dispatcher.dispatch_ws_event(ws_event)
        assert rest_adapter.post_reply.called

    asyncio.run(_test())
