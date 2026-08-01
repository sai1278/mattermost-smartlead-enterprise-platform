import pytest


@pytest.fixture
def sample_headers():
    return {"X-Custom": "test-val"}
