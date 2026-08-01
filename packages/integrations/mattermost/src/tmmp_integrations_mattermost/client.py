"""Mattermost Enterprise REST API Client."""

from __future__ import annotations

from typing import Any

from tmmp_integrations_shared.client import BaseAsyncHTTPClient
from tmmp_integrations_shared.dto import Result
from tmmp_integrations_shared.errors import IntegrationError

from tmmp_integrations_mattermost.auth import MattermostAuth
from tmmp_integrations_mattermost.config import MattermostConfig
from tmmp_integrations_mattermost.dto import ChannelDTO, PostDTO, TeamDTO, UserDTO
from tmmp_integrations_mattermost.endpoints import Routes
from tmmp_integrations_mattermost.telemetry import mattermost_span


class MattermostClient(BaseAsyncHTTPClient):
    """SDK client for interacting with Mattermost REST API v4."""

    def __init__(self, config: MattermostConfig) -> None:
        auth = MattermostAuth(bot_token=config.bot_token.get_secret_value())
        super().__init__(
            base_url=config.mattermost_url,
            auth_strategy=auth,
            service_name="mattermost-sdk",
        )
        self.config = config

    async def ping(self) -> Result[dict[str, Any], IntegrationError]:
        async with mattermost_span("ping"):
            return await self.get(Routes.PING)

    async def create_post(
        self,
        channel_id: str,
        message: str,
        root_id: str = "",
        props: dict[str, Any] | None = None,
    ) -> Result[PostDTO, IntegrationError]:
        async with mattermost_span("create_post", {"channel_id": channel_id}):
            payload: dict[str, Any] = {
                "channel_id": channel_id,
                "message": message,
            }
            if root_id:
                payload["root_id"] = root_id
            if props:
                payload["props"] = props

            res = await self.post(Routes.POSTS, json_data=payload)
            if res.is_ok:
                return Result.ok(PostDTO.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("create_post failed"))

    async def get_post(self, post_id: str) -> Result[PostDTO, IntegrationError]:
        async with mattermost_span("get_post", {"post_id": post_id}):
            res = await self.get(Routes.post_details(post_id))
            if res.is_ok:
                return Result.ok(PostDTO.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("get_post failed"))

    async def get_channel(self, channel_id: str) -> Result[ChannelDTO, IntegrationError]:
        async with mattermost_span("get_channel", {"channel_id": channel_id}):
            res = await self.get(Routes.channel_details(channel_id))
            if res.is_ok:
                return Result.ok(ChannelDTO.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("get_channel failed"))

    async def get_channel_by_name(
        self,
        team_id: str,
        name: str,
    ) -> Result[ChannelDTO, IntegrationError]:
        async with mattermost_span("get_channel_by_name", {"name": name}):
            res = await self.get(Routes.channel_by_name(team_id, name))
            if res.is_ok:
                return Result.ok(ChannelDTO.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("get_channel_by_name failed"))

    async def create_direct_channel(
        self,
        user_id_1: str,
        user_id_2: str,
    ) -> Result[ChannelDTO, IntegrationError]:
        async with mattermost_span("create_direct_channel"):
            payload = [user_id_1, user_id_2]
            res = await self.post(Routes.direct_channel(), json_data=payload)  # type: ignore[arg-type]
            if res.is_ok:
                return Result.ok(ChannelDTO.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("create_direct_channel failed"))

    async def get_user_by_username(
        self,
        username: str,
    ) -> Result[UserDTO, IntegrationError]:
        async with mattermost_span("get_user_by_username", {"username": username}):
            user = username.lstrip("@")
            res = await self.get(Routes.user_by_username(user))
            if res.is_ok:
                return Result.ok(UserDTO.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("get_user_by_username failed"))

    async def get_me(self) -> Result[UserDTO, IntegrationError]:
        async with mattermost_span("get_me"):
            res = await self.get(Routes.USERS_ME)
            if res.is_ok:
                return Result.ok(UserDTO.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("get_me failed"))

    async def get_team(self, team_id: str) -> Result[TeamDTO, IntegrationError]:
        async with mattermost_span("get_team", {"team_id": team_id}):
            res = await self.get(Routes.team_details(team_id))
            if res.is_ok:
                return Result.ok(TeamDTO.model_validate(res.unwrap()))
            return Result.fail(res.error() or IntegrationError("get_team failed"))
