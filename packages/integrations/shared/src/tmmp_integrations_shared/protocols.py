"""Shared Protocols and Interfaces."""

from __future__ import annotations

from typing import Any, Protocol, TypeVar

from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError

T = TypeVar("T")


class HTTPClientProtocol(Protocol):
    """Protocol defining standard async HTTP client interface."""

    async def get(
        self,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> Result[dict[str, Any], IntegrationError]: ...

    async def post(
        self,
        url: str,
        json_data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> Result[dict[str, Any], IntegrationError]: ...
