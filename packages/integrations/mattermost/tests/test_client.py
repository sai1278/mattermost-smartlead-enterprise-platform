import asyncio

from tmmp_integrations_mattermost.client import MattermostClient
from tmmp_integrations_mattermost.config import MattermostConfig


def test_client_init_and_routes(mock_config: MattermostConfig):
    client = MattermostClient(mock_config)
    assert client.base_url == "http://localhost:8065"

    async def _test():
        await client.close()

    asyncio.run(_test())
