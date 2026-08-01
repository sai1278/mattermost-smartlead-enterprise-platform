"""Authentication Abstractions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AuthStrategy(ABC):
    """Abstract base class for API authentication strategies."""

    @abstractmethod
    async def get_headers(self) -> dict[str, str]:
        """Return headers required for authentication."""

    @abstractmethod
    async def get_params(self) -> dict[str, Any]:
        """Return URL parameters required for authentication."""


class BearerTokenAuth(AuthStrategy):
    """HTTP Bearer Token Authentication Strategy."""

    def __init__(self, token: str) -> None:
        self._token = token

    async def get_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    async def get_params(self) -> dict[str, Any]:
        return {}


class APIKeyAuth(AuthStrategy):
    """API Key Authentication Strategy (Header or Query Param)."""

    def __init__(
        self,
        api_key: str,
        header_name: str = "X-API-Key",
        in_query: bool = False,
    ) -> None:
        self._api_key = api_key
        self._header_name = header_name
        self._in_query = in_query

    async def get_headers(self) -> dict[str, str]:
        if not self._in_query:
            return {self._header_name: self._api_key}
        return {}

    async def get_params(self) -> dict[str, Any]:
        if self._in_query:
            return {self._header_name: self._api_key}
        return {}
