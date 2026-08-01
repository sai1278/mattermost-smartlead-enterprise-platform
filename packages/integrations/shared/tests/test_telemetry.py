from tmmp_integrations_shared.context import get_correlation_id, set_correlation_id
from tmmp_integrations_shared.logging import get_logger
from tmmp_integrations_shared.metrics import MetricsCollector


def test_correlation_id():
    cid = get_correlation_id()
    assert len(cid) > 0
    set_correlation_id("custom-cid-123")
    assert get_correlation_id() == "custom-cid-123"


def test_logger():
    logger = get_logger("test_logger")
    assert logger.name == "test_logger"


def test_metrics_collector():
    collector = MetricsCollector(service_name="unit-test-svc")
    collector.record_request(method="GET", status_code=200, duration_seconds=0.05)
