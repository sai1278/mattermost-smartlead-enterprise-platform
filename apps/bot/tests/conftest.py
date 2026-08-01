import pytest
from pydantic import SecretStr
from tmmp_mattermost_bot.config import BotConfig


@pytest.fixture
def mock_bot_config():
    return BotConfig(
        mattermost_url="http://localhost:8065",
        ws_url="ws://localhost:8065",
        bot_token=SecretStr("bot-token-123"),
        bot_username="testbot",
        digest_channel_id="channel-digest-101",
    )
