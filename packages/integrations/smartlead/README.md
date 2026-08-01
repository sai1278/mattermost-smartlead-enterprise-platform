# Smartlead Enterprise Integration SDK (`tmmp-integrations-smartlead`)

Production-grade, typed Python SDK for Smartlead v1 REST API and Webhook event processing. Reuses `tmmp-integrations-shared` for resilience, metrics, tracing, and monadic error handling.

## Components Included

- **`SmartleadClient`**: Async HTTP client for Campaigns, Email Accounts, Warmup Status, Pause/Resume, and Reputation metrics.
- **`SmartleadWebhookValidator`**: HMAC SHA256 signature verification & typed event deserialization.
- **`SmartleadPaginator`**: Async iterator for paginated endpoints.
- **`SmartleadHealthCheck`**: Service health probe implementation.

## Usage Example

```python
import asyncio
from pydantic import SecretStr
from tmmp_integrations_smartlead import SmartleadClient, SmartleadConfig

async def main():
    config = SmartleadConfig(
        smartlead_api_url="https://server.smartlead.ai/api/v1",
        api_key=SecretStr("your-api-key"),
    )
    client = SmartleadClient(config)

    res = await client.list_campaigns()
    if res.is_ok:
        campaigns = res.unwrap()
        print(f"Found {len(campaigns)} campaigns.")
    else:
        print("Error fetching campaigns:", res.error())

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```
