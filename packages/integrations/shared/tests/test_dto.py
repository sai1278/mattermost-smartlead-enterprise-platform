import pytest
from tmmp_integrations_shared.dto import BaseDTO, PaginatedResponse, Result


class SampleDTO(BaseDTO):
    id: str
    name: str


def test_base_dto():
    dto = SampleDTO(id="1", name="test")
    assert dto.id == "1"
    assert dto.name == "test"


def test_paginated_response():
    dto = SampleDTO(id="1", name="test")
    resp = PaginatedResponse[SampleDTO](
        items=[dto], total_count=1, page=1, page_size=10, has_more=False
    )
    assert len(resp.items) == 1
    assert resp.total_count == 1
    assert not resp.has_more


def test_result_ok():
    res = Result[str, ValueError].ok("hello")
    assert res.is_ok
    assert not res.is_fail
    assert res.unwrap() == "hello"
    assert res.error() is None


def test_result_fail():
    err = ValueError("bad input")
    res = Result[str, ValueError].fail(err)
    assert res.is_fail
    assert not res.is_ok
    assert res.error() == err
    with pytest.raises(ValueError):
        res.unwrap()


def test_result_invalid():
    with pytest.raises(ValueError):
        Result[str, ValueError](value="a", error=ValueError("b"))
    with pytest.raises(ValueError):
        Result[str, ValueError](value=None, error=None)
