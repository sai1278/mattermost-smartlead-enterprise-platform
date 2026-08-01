import pytest
from pydantic import SecretStr
from tmmp_integrations_smartlead.config import SmartleadConfig


@pytest.fixture
def mock_config():
    return SmartleadConfig(
        smartlead_api_url="https://server.smartlead.ai/api/v1",
        api_key=SecretStr("test-api-key-123"),
    )
