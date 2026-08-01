"""Base Async HTTP Client Implementation."""

from __future__ import annotations

import time
from typing import Any

import httpx

from tmmp_integrations_shared.auth import AuthStrategy
from tmmp_integrations_shared.context import get_correlation_id
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import (
    AuthenticationError,
    HTTPError,
    IntegrationError,
    RateLimitError,
)
from tmmp_integrations_shared.errors import (
    TimeoutError as SharedTimeoutError,
)
from tmmp_integrations_shared.logging import get_logger
from tmmp_integrations_shared.metrics import MetricsCollector
from tmmp_integrations_shared.resilience import (
    CircuitBreaker,
    RetryPolicy,
    TimeoutConfig,
    TokenBucketRateLimiter,
)

LOGGER = get_logger(__name__)


class BaseAsyncHTTPClient:
    """Production-grade async HTTP client wrapper with resilience features."""

    def __init__(
        self,
        base_url: str,
        auth_strategy: AuthStrategy | None = None,
        retry_policy: RetryPolicy | None = None,
        circuit_breaker: CircuitBreaker | None = None,
        rate_limiter: TokenBucketRateLimiter | None = None,
        timeout_config: TimeoutConfig | None = None,
        service_name: str = "base-http-client",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth_strategy = auth_strategy
        self.retry_policy = retry_policy or RetryPolicy()
        self.circuit_breaker = circuit_breaker or CircuitBreaker(name=service_name)
        self.rate_limiter = rate_limiter
        self.timeout_config = timeout_config or TimeoutConfig()
        self.service_name = service_name
        self.metrics = MetricsCollector(service_name=service_name)

        timeout = httpx.Timeout(
            connect=self.timeout_config.connect,
            read=self.timeout_config.read,
            write=self.timeout_config.write,
            pool=self.timeout_config.total,
        )
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout)

    async def close(self) -> None:
        """Close underlying httpx client."""
        await self._client.aclose()

    async def _execute_request(
        self,
        method: str,
        path: str,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Result[dict[str, Any], IntegrationError]:
        """Execute request with retry, circuit breaker, and rate limiter protection."""
        self.circuit_breaker.check_state()

        if self.rate_limiter:
            await self.rate_limiter.acquire()

        req_headers = headers or {}
        req_params = params or {}
        req_headers["X-Correlation-ID"] = get_correlation_id()

        if self.auth_strategy:
            auth_h = await self.auth_strategy.get_headers()
            auth_p = await self.auth_strategy.get_params()
            req_headers.update(auth_h)
            req_params.update(auth_p)

        attempts = self.retry_policy.max_attempts
        last_error: IntegrationError | None = None

        for attempt in range(1, attempts + 1):
            if attempt > 1:
                delay = self.retry_policy.calculate_backoff(attempt)
                time.sleep(delay)

            start_time = time.monotonic()
            try:
                response = await self._client.request(
                    method=method,
                    url=path,
                    json=json_data,
                    headers=req_headers,
                    params=req_params,
                )
                duration = time.monotonic() - start_time
                self.metrics.record_request(method, response.status_code, duration)

                if response.status_code in (401, 403):
                    auth_err: IntegrationError = AuthenticationError(
                        "Auth failed", status_code=response.status_code
                    )
                    self.circuit_breaker.record_failure()
                    return Result.fail(auth_err)

                if response.status_code == 429:
                    rl_err: IntegrationError = RateLimitError(
                        "Rate limit exceeded", status_code=429
                    )
                    self.circuit_breaker.record_failure()
                    last_error = rl_err
                    continue

                if response.is_error:
                    http_err: IntegrationError = HTTPError(
                        "HTTP error",
                        status_code=response.status_code,
                        response_body=response.text,
                    )
                    self.circuit_breaker.record_failure()
                    last_error = http_err
                    continue

                self.circuit_breaker.record_success()
                data = response.json() if response.text else {}
                return Result.ok(data)

            except httpx.TimeoutException as exc:
                self.circuit_breaker.record_failure()
                last_error = SharedTimeoutError(f"Request timeout: {exc}")
            except Exception as exc:
                self.circuit_breaker.record_failure()
                last_error = IntegrationError(f"Request failed: {exc}")

        return Result.fail(last_error or IntegrationError("Request failed after retries"))

    async def get(
        self,
        path: str,
        headers: dict[str, str] | None = None,
    ) -> Result[dict[str, Any], IntegrationError]:
        return await self._execute_request("GET", path, headers=headers)

    async def post(
        self,
        path: str,
        json_data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> Result[dict[str, Any], IntegrationError]:
        return await self._execute_request("POST", path, json_data=json_data, headers=headers)
