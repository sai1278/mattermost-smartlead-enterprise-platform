# Shared Integration Platform Foundation (`tmmp-integrations-shared`)

Enterprise-grade shared foundation for microservices and integration SDKs within the platform monorepo.

## Architecture & Features

- **Base Async HTTP Client:** `BaseAsyncHTTPClient` wrapping `httpx.AsyncClient` with built-in resilience.
- **Resilience Controls:** Exponential backoff retry with jitter (`RetryPolicy`), stateful circuit breaker (`CircuitBreaker`), token-bucket rate limiter (`TokenBucketRateLimiter`).
- **Auth Strategies:** Pluggable `AuthStrategy`, `BearerTokenAuth`, `APIKeyAuth`.
- **Domain Result Types:** Monadic `Result[T, E]` and generic `PaginatedResponse[T]`.
- **Observability:** Structured JSON logger, Prometheus metrics collector, OpenTelemetry tracing spans, and correlation ID propagation.
- **Health Checks & Flags:** `HealthCheckResult`, `HealthStatus`, `FeatureFlagProvider`.

## Usage Example

```python
import asyncio
from tmmp_integrations_shared import BaseAsyncHTTPClient, BearerTokenAuth

async def main():
    auth = BearerTokenAuth("secret-token")
    client = BaseAsyncHTTPClient(base_url="https://api.example.com", auth_strategy=auth)
    result = await client.get("/v1/data")
    if result.is_ok:
        print("Success:", result.unwrap())
    else:
        print("Failed:", result.error())
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```
