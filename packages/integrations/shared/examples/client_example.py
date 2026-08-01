"""Example usage of BaseAsyncHTTPClient from tmmp-integrations-shared."""

import asyncio

from tmmp_integrations_shared import (
    APIKeyAuth,
    BaseAsyncHTTPClient,
    CircuitBreaker,
    RetryPolicy,
    TokenBucketRateLimiter,
)


async def run_example() -> None:
    auth = APIKeyAuth("api-key-value", header_name="X-API-Key")
    retry = RetryPolicy(max_attempts=3, initial_backoff=0.5)
    circuit = CircuitBreaker(failure_threshold=5, name="example-service")
    limiter = TokenBucketRateLimiter(rate=10.0, capacity=20.0)

    client = BaseAsyncHTTPClient(
        base_url="https://api.example.com",
        auth_strategy=auth,
        retry_policy=retry,
        circuit_breaker=circuit,
        rate_limiter=limiter,
        service_name="example-client",
    )

    print("Executing GET request...")
    result = await client.get("/v1/resource")

    if result.is_ok:
        print("Success payload:", result.unwrap())
    else:
        print("Failed with error:", result.error())

    await client.close()


if __name__ == "__main__":
    asyncio.run(run_example())
