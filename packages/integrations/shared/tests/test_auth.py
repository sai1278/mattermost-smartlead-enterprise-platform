import asyncio

from tmmp_integrations_shared.auth import APIKeyAuth, BearerTokenAuth


def test_bearer_token_auth():
    async def _test():
        auth = BearerTokenAuth("secret123")
        headers = await auth.get_headers()
        params = await auth.get_params()
        assert headers == {"Authorization": "Bearer secret123"}
        assert params == {}

    asyncio.run(_test())


def test_api_key_auth_header():
    async def _test():
        auth = APIKeyAuth("key123", header_name="X-API-Key", in_query=False)
        headers = await auth.get_headers()
        params = await auth.get_params()
        assert headers == {"X-API-Key": "key123"}
        assert params == {}

    asyncio.run(_test())


def test_api_key_auth_query():
    async def _test():
        auth = APIKeyAuth("key123", header_name="api_key", in_query=True)
        headers = await auth.get_headers()
        params = await auth.get_params()
        assert headers == {}
        assert params == {"api_key": "key123"}

    asyncio.run(_test())
