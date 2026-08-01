import asyncio
from unittest.mock import AsyncMock, MagicMock

from tmmp_command_handler.application.dispatcher import CommandDispatcher
from tmmp_command_handler.application.warmup_commands import WarmupCommandHandler
from tmmp_integrations_mattermost import SlashCommandPayload, SlashCommandResponse


def test_command_dispatcher_routing():
    handler = MagicMock(spec=WarmupCommandHandler)
    dummy_resp = SlashCommandResponse(response_type="ephemeral", text="help output")
    handler.handle_command = AsyncMock(return_value=dummy_resp)

    dispatcher = CommandDispatcher(handler)
    payload = SlashCommandPayload(
        channel_id="c1",
        channel_name="town-square",
        command="/warmup",
        response_url="http://localhost/resp",
        team_id="t1",
        text="help",
        user_id="u1",
        user_name="bob",
    )

    async def _test():
        res = await dispatcher.dispatch(payload)
        assert res.text == "help output"
        assert handler.handle_command.called

    asyncio.run(_test())
