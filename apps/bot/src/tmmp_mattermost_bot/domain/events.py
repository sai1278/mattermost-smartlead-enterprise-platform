"""Mattermost Bot Domain Events."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BotEvent:
    event_type: str


@dataclass(frozen=True)
class BotMessageReceived(BotEvent):
    post_id: str
    channel_id: str
    user_id: str
    message: str
    root_id: str = ""


@dataclass(frozen=True)
class BotUserMentioned(BotEvent):
    post_id: str
    channel_id: str
    user_id: str
    message: str
