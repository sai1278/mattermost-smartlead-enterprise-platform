"""Shared Integration Platform Package Public API."""

from tmmp_integrations_shared.auth import APIKeyAuth, AuthStrategy, BearerTokenAuth
from tmmp_integrations_shared.client import BaseAsyncHTTPClient
from tmmp_integrations_shared.config import BaseIntegrationConfig
from tmmp_integrations_shared.context import RequestContext, get_correlation_id, set_correlation_id
from tmmp_integrations_shared.dto import BaseDTO, PaginatedResponse, Result
from tmmp_integrations_shared.errors import (
    AuthenticationError,
    CircuitBreakerError,
    HTTPError,
    IntegrationError,
    RateLimitError,
    TimeoutError,
)
from tmmp_integrations_shared.flags import FeatureFlagProvider, InMemoryFeatureFlagProvider
from tmmp_integrations_shared.health import HealthCheckResult, HealthStatus
from tmmp_integrations_shared.logging import get_logger
from tmmp_integrations_shared.metrics import MetricsCollector
from tmmp_integrations_shared.resilience import (
    CircuitBreaker,
    RetryPolicy,
    TimeoutConfig,
    TokenBucketRateLimiter,
)
from tmmp_integrations_shared.telemetry import get_tracer, trace_span

__all__ = [
    "APIKeyAuth",
    "AuthStrategy",
    "BearerTokenAuth",
    "BaseAsyncHTTPClient",
    "BaseDTO",
    "BaseIntegrationConfig",
    "CircuitBreaker",
    "CircuitBreakerError",
    "FeatureFlagProvider",
    "HealthCheckResult",
    "HealthStatus",
    "HTTPError",
    "AuthenticationError",
    "InMemoryFeatureFlagProvider",
    "IntegrationError",
    "MetricsCollector",
    "PaginatedResponse",
    "RateLimitError",
    "RequestContext",
    "Result",
    "RetryPolicy",
    "TimeoutConfig",
    "TimeoutError",
    "TokenBucketRateLimiter",
    "get_correlation_id",
    "get_logger",
    "get_tracer",
    "set_correlation_id",
    "trace_span",
]
