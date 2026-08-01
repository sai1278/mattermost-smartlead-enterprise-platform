"""Mattermost SDK Authentication Strategy."""

from __future__ import annotations

from tmmp_integrations_shared.auth import BearerTokenAuth


class MattermostAuth(BearerTokenAuth):
    """Mattermost Bearer Token Authentication."""

    def __init__(self, bot_token: str) -> None:
        super().__init__(token=bot_token)
