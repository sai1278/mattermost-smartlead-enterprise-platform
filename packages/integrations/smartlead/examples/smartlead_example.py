"""Example usage of Smartlead Enterprise SDK."""

import asyncio

from pydantic import SecretStr
from tmmp_integrations_smartlead import SmartleadClient, SmartleadConfig


async def run_example() -> None:
    config = SmartleadConfig(
        smartlead_api_url="https://server.smartlead.ai/api/v1",
        api_key=SecretStr("example-api-key"),
    )
    client = SmartleadClient(config)

    print("Fetching campaigns...")
    res = await client.list_campaigns()
    if res.is_ok:
        print("Campaigns:", res.unwrap())
    else:
        print("Failed:", res.error())

    await client.close()


if __name__ == "__main__":
    asyncio.run(run_example())
