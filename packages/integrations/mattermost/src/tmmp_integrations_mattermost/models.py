"""Mattermost Domain Enums and Core Value Objects."""

from __future__ import annotations

from enum import Enum


class ChannelType(Enum):
    PUBLIC = "O"
    PRIVATE = "P"
    DIRECT = "D"
    GROUP = "G"


class PostType(Enum):
    DEFAULT = ""
    SYSTEM_GENERIC = "system_generic"
    SLACK_ATTACHMENT = "slack_attachment"
