import asyncio

from tmmp_integrations_shared.auth import BearerTokenAuth
from tmmp_integrations_shared.client import BaseAsyncHTTPClient


def test_client_init_and_close():
    async def _test():
        auth = BearerTokenAuth("my-token")
        client = BaseAsyncHTTPClient(
            base_url="https://httpbin.org",
            auth_strategy=auth,
            service_name="test-client",
        )
        assert client.base_url == "https://httpbin.org"
        await client.close()

    asyncio.run(_test())
