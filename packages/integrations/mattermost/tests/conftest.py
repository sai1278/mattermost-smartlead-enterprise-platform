import pytest
from pydantic import SecretStr
from tmmp_integrations_mattermost.config import MattermostConfig


@pytest.fixture
def mock_config():
    return MattermostConfig(
        mattermost_url="http://localhost:8065",
        bot_token=SecretStr("mock-token-123"),
        team_id="team-id-456",
    )
