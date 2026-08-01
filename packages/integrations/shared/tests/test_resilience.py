import asyncio

import pytest
from tmmp_integrations_shared.errors import CircuitBreakerError
from tmmp_integrations_shared.resilience import (
    CircuitBreaker,
    CircuitState,
    RetryPolicy,
    TimeoutConfig,
    TokenBucketRateLimiter,
)


def test_retry_policy():
    policy = RetryPolicy(max_attempts=3, initial_backoff=1.0, backoff_factor=2.0, jitter=False)
    assert policy.calculate_backoff(1) == 0.0
    assert policy.calculate_backoff(2) == 1.0
    assert policy.calculate_backoff(3) == 2.0


def test_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1, name="test-cb")
    assert cb.state == CircuitState.CLOSED
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    with pytest.raises(CircuitBreakerError):
        cb.check_state()


def test_timeout_config():
    cfg = TimeoutConfig(connect=2.0, read=5.0, write=5.0, total=10.0)
    assert cfg.connect == 2.0
    assert cfg.total == 10.0


def test_rate_limiter():
    async def _test():
        limiter = TokenBucketRateLimiter(rate=100.0, capacity=10.0)
        await limiter.acquire(1.0)
        assert limiter.tokens <= 10.0

    asyncio.run(_test())
