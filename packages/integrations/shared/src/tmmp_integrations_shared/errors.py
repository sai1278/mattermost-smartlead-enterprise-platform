"""Shared Integration Exception Hierarchy."""

from __future__ import annotations

from typing import Any


class IntegrationError(Exception):
    """Base exception for all integration errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class HTTPError(IntegrationError):
    """Raised when an HTTP request fails."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_body: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, details)
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(HTTPError):
    """Raised when authentication fails (HTTP 401/403)."""


class RateLimitError(HTTPError):
    """Raised when request is rate limited (HTTP 429)."""

    def __init__(
        self,
        message: str,
        status_code: int = 429,
        retry_after: float | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, details=details)
        self.retry_after = retry_after


class TimeoutError(IntegrationError):
    """Raised when an operation times out."""


class CircuitBreakerError(IntegrationError):
    """Raised when circuit breaker is OPEN."""
