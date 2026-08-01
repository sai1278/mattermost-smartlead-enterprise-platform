"""Resilience Patterns: Retry Policy, Circuit Breaker, Rate Limiter, Timeout Config."""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass
from enum import Enum

from tmmp_integrations_shared.errors import (
    CircuitBreakerError,
)


@dataclass(frozen=True)
class TimeoutConfig:
    """Timeout configuration for HTTP requests."""

    connect: float = 5.0
    read: float = 10.0
    write: float = 10.0
    total: float = 30.0


@dataclass(frozen=True)
class RetryPolicy:
    """Retry policy configuration with exponential backoff and jitter."""

    max_attempts: int = 3
    initial_backoff: float = 0.5
    max_backoff: float = 10.0
    backoff_factor: float = 2.0
    jitter: bool = True

    def calculate_backoff(self, attempt: int) -> float:
        """Calculate backoff delay for given attempt (1-indexed)."""
        if attempt <= 1:
            return 0.0
        delay = self.initial_backoff * (self.backoff_factor ** (attempt - 2))
        delay = min(delay, self.max_backoff)
        if self.jitter:
            delay = delay * (0.5 + random.random())
        return delay


class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    """Stateful Circuit Breaker for resilience."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        name: str = "default",
    ) -> None:
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_state_change = time.monotonic()

    @property
    def state(self) -> CircuitState:
        now = time.monotonic()
        if (
            self._state == CircuitState.OPEN
            and now - self._last_state_change >= self.recovery_timeout
        ):
            self._state = CircuitState.HALF_OPEN
            self._last_state_change = now
        return self._state

    def record_success(self) -> None:
        self._failure_count = 0
        if self._state != CircuitState.CLOSED:
            self._state = CircuitState.CLOSED
            self._last_state_change = time.monotonic()

    def record_failure(self) -> None:
        self._failure_count += 1
        if self._failure_count >= self.failure_threshold and self._state != CircuitState.OPEN:
            self._state = CircuitState.OPEN
            self._last_state_change = time.monotonic()

    def check_state(self) -> None:
        if self.state == CircuitState.OPEN:
            raise CircuitBreakerError(f"Circuit breaker '{self.name}' is OPEN. Requests blocked.")


class TokenBucketRateLimiter:
    """Async Token Bucket Rate Limiter."""

    def __init__(self, rate: float, capacity: float) -> None:
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> None:
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.last_update = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)

            if self.tokens < tokens:
                needed = tokens - self.tokens
                wait_time = needed / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0.0
            else:
                self.tokens -= tokens
