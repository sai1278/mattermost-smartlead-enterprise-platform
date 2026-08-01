"""Mattermost REST API v4 Routes."""

from __future__ import annotations


class Routes:
    """Mattermost v4 API Route Constants."""

    PING = "/api/v4/system/ping"
    USERS = "/api/v4/users"
    USERS_ME = "/api/v4/users/me"
    POSTS = "/api/v4/posts"
    CHANNELS = "/api/v4/channels"
    TEAMS = "/api/v4/teams"
    FILES = "/api/v4/files"

    @staticmethod
    def post_details(post_id: str) -> str:
        return f"/api/v4/posts/{post_id}"

    @staticmethod
    def channel_details(channel_id: str) -> str:
        return f"/api/v4/channels/{channel_id}"

    @staticmethod
    def channel_by_name(team_id: str, name: str) -> str:
        return f"/api/v4/teams/{team_id}/channels/name/{name}"

    @staticmethod
    def direct_channel() -> str:
        return "/api/v4/channels/direct"

    @staticmethod
    def user_by_username(username: str) -> str:
        return f"/api/v4/users/username/{username}"

    @staticmethod
    def user_details(user_id: str) -> str:
        return f"/api/v4/users/{user_id}"

    @staticmethod
    def team_by_name(name: str) -> str:
        return f"/api/v4/teams/name/{name}"

    @staticmethod
    def team_details(team_id: str) -> str:
        return f"/api/v4/teams/{team_id}"
