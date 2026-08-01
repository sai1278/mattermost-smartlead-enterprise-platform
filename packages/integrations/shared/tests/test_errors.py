from tmmp_integrations_shared.errors import (
    AuthenticationError,
    CircuitBreakerError,
    HTTPError,
    IntegrationError,
    RateLimitError,
    TimeoutError,
)


def test_integration_error():
    err = IntegrationError("base error", details={"key": "val"})
    assert str(err) == "base error"
    assert err.details == {"key": "val"}


def test_http_error():
    err = HTTPError("not found", status_code=404, response_body="err body")
    assert err.status_code == 404
    assert err.response_body == "err body"


def test_auth_error():
    err = AuthenticationError("unauthorized", status_code=401)
    assert isinstance(err, HTTPError)
    assert err.status_code == 401


def test_rate_limit_error():
    err = RateLimitError("too many requests", retry_after=5.0)
    assert err.status_code == 429
    assert err.retry_after == 5.0


def test_timeout_and_circuit_errors():
    t_err = TimeoutError("timeout")
    c_err = CircuitBreakerError("circuit open")
    assert isinstance(t_err, IntegrationError)
    assert isinstance(c_err, IntegrationError)
