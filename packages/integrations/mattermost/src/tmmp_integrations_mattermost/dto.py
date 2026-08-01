"""Mattermost SDK Data Transfer Objects."""

from __future__ import annotations

from typing import Any

from pydantic import Field
from tmmp_integrations_shared.dto import BaseDTO


class UserDTO(BaseDTO):
    id: str
    username: str
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    roles: str = ""


class ChannelDTO(BaseDTO):
    id: str
    team_id: str = ""
    type: str
    name: str
    display_name: str = ""
    header: str = ""
    purpose: str = ""


class PostDTO(BaseDTO):
    id: str
    channel_id: str
    user_id: str
    message: str
    root_id: str = ""
    file_ids: list[str] = Field(default_factory=list)
    create_at: int = 0
    props: dict[str, Any] = Field(default_factory=dict)


class TeamDTO(BaseDTO):
    id: str
    name: str
    display_name: str = ""
    type: str = "O"


class FileUploadResultDTO(BaseDTO):
    file_infos: list[dict[str, Any]] = Field(default_factory=list)
    client_ids: list[str] = Field(default_factory=list)


class SlashCommandPayload(BaseDTO):
    channel_id: str
    channel_name: str
    command: str
    response_url: str
    team_id: str
    text: str
    user_id: str
    user_name: str
    trigger_id: str = ""


class SlashCommandResponse(BaseDTO):
    response_type: str = "in_channel"  # or "ephemeral"
    text: str
    username: str | None = None
    icon_url: str | None = None
    attachments: list[dict[str, Any]] = Field(default_factory=list)
