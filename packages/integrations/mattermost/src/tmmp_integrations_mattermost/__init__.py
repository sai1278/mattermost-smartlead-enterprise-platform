"""Mattermost Integration SDK Package Public API."""

from tmmp_integrations_mattermost.attachments import InteractiveAttachmentBuilder
from tmmp_integrations_mattermost.auth import MattermostAuth
from tmmp_integrations_mattermost.client import MattermostClient
from tmmp_integrations_mattermost.config import MattermostConfig
from tmmp_integrations_mattermost.dto import (
    ChannelDTO,
    FileUploadResultDTO,
    PostDTO,
    SlashCommandPayload,
    SlashCommandResponse,
    TeamDTO,
    UserDTO,
)
from tmmp_integrations_mattermost.endpoints import Routes
from tmmp_integrations_mattermost.errors import (
    MattermostAPIError,
    MattermostAuthError,
    MattermostSDKError,
    MattermostWebSocketError,
)
from tmmp_integrations_mattermost.health import MattermostHealthCheck
from tmmp_integrations_mattermost.markdown import MarkdownBuilder
from tmmp_integrations_mattermost.models import ChannelType, PostType
from tmmp_integrations_mattermost.websocket import (
    MattermostWebSocketClient,
    MattermostWebSocketEvent,
)

__all__ = [
    "ChannelDTO",
    "ChannelType",
    "FileUploadResultDTO",
    "InteractiveAttachmentBuilder",
    "MarkdownBuilder",
    "MattermostAPIError",
    "MattermostAuth",
    "MattermostAuthError",
    "MattermostClient",
    "MattermostConfig",
    "MattermostHealthCheck",
    "MattermostSDKError",
    "MattermostWebSocketClient",
    "MattermostWebSocketEvent",
    "MattermostWebSocketError",
    "PostDTO",
    "PostType",
    "Routes",
    "SlashCommandPayload",
    "SlashCommandResponse",
    "TeamDTO",
    "UserDTO",
]
