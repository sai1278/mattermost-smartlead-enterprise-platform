"""Mattermost SDK Exception Classes."""

from __future__ import annotations

from tmmp_integrations_shared.errors import AuthenticationError, HTTPError, IntegrationError


class MattermostSDKError(IntegrationError):
    """Base error for Mattermost SDK."""


class MattermostAPIError(HTTPError, MattermostSDKError):
    """Raised when Mattermost REST API returns an error."""


class MattermostAuthError(AuthenticationError, MattermostSDKError):
    """Raised when Mattermost authentication fails."""


class MattermostWebSocketError(MattermostSDKError):
    """Raised when Mattermost WebSocket client encounters an error."""
