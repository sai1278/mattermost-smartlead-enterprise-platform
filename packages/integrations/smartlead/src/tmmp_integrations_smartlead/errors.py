"""Smartlead SDK Exception Classes."""

from __future__ import annotations

from tmmp_integrations_shared.errors import AuthenticationError, HTTPError, IntegrationError


class SmartleadSDKError(IntegrationError):
    """Base error for Smartlead SDK."""


class SmartleadAPIError(HTTPError, SmartleadSDKError):
    """Raised when Smartlead REST API returns an error."""


class SmartleadAuthError(AuthenticationError, SmartleadSDKError):
    """Raised when Smartlead API key authentication fails."""


class SmartleadWebhookValidationError(SmartleadSDKError):
    """Raised when Smartlead webhook signature validation fails."""
