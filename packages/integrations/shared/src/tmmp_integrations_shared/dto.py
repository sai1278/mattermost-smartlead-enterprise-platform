"""Domain Result Types and Typed Base DTOs."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class BaseDTO(BaseModel):
    """Base Pydantic model for integration Data Transfer Objects."""

    model_config = ConfigDict(
        frozen=True,
        extra="ignore",
        populate_by_name=True,
    )


class PaginatedResponse(BaseDTO, Generic[T]):
    """Generic container for paginated API responses."""

    items: list[T]
    total_count: int
    page: int = 1
    page_size: int = 50
    has_more: bool = False


class Result(Generic[T, E]):
    """Monadic Result type for explicit, type-safe error handling."""

    def __init__(self, value: T | None = None, error: E | None = None) -> None:
        if value is not None and error is not None:
            raise ValueError("Result cannot contain both value and error")
        if value is None and error is None:
            raise ValueError("Result must contain either value or error")
        self._value = value
        self._error = error

    @classmethod
    def ok(cls, value: T) -> Result[T, E]:
        return cls(value=value)

    @classmethod
    def fail(cls, error: E) -> Result[T, E]:
        return cls(error=error)

    @property
    def is_ok(self) -> bool:
        return self._value is not None

    @property
    def is_fail(self) -> bool:
        return self._error is not None

    def unwrap(self) -> T:
        if self._error is not None:
            raise self._error
        assert self._value is not None
        return self._value

    def error(self) -> E | None:
        return self._error
