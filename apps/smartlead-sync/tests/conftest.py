import pytest
from tmmp_smartlead_sync.domain.entities import WarmupMetricsSnapshot
from tmmp_smartlead_sync.infrastructure.in_memory_repository import InMemoryWarmupRepository


@pytest.fixture
def repository():
    return InMemoryWarmupRepository()


@pytest.fixture
def sample_healthy_snapshot():
    return WarmupMetricsSnapshot(
        account_id=101,
        email="sender@company.com",
        sent_count=100,
        inbox_count=98,
        spam_count=1,
        bounce_count=1,
        inbox_rate=98.0,
        spam_rate=1.0,
        bounce_rate=1.0,
    )
