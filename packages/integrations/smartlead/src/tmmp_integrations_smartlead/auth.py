"""Smartlead SDK Authentication Strategy."""

from __future__ import annotations

from tmmp_integrations_shared.auth import APIKeyAuth


class SmartleadAuth(APIKeyAuth):
    """Smartlead API Key Authentication via URL query parameter."""

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key, header_name="api_key", in_query=True)
