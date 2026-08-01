import asyncio

from tmmp_integrations_smartlead.client import SmartleadClient
from tmmp_integrations_smartlead.config import SmartleadConfig


def test_client_init(mock_config: SmartleadConfig):
    client = SmartleadClient(mock_config)
    assert client.base_url == "https://server.smartlead.ai/api/v1"

    async def _test():
        await client.close()

    asyncio.run(_test())
