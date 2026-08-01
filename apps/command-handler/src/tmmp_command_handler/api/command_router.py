"""FastAPI APIRouter for Mattermost Slash Commands."""

from __future__ import annotations

from fastapi import APIRouter, Form, HTTPException, status
from tmmp_command_handler.application.dispatcher import CommandDispatcher
from tmmp_command_handler.domain.authorization import CommandAuthorizationPolicy
from tmmp_integrations_mattermost import SlashCommandPayload, SlashCommandResponse

router = APIRouter(prefix="/api/v1/commands", tags=["commands"])

_dispatcher_instance: CommandDispatcher | None = None
_expected_token: str = "mattermost-verification-token"


def set_command_dispatcher(dispatcher: CommandDispatcher, verification_token: str) -> None:
    global _dispatcher_instance, _expected_token
    _dispatcher_instance = dispatcher
    _expected_token = verification_token


@router.post("/smartlead", response_model=SlashCommandResponse)
async def handle_smartlead_slash_command(
    channel_id: str = Form(""),
    channel_name: str = Form(""),
    command: str = Form(""),
    response_url: str = Form(""),
    team_id: str = Form(""),
    text: str = Form(""),
    token: str = Form(""),
    user_id: str = Form(""),
    user_name: str = Form(""),
    trigger_id: str = Form(""),
) -> SlashCommandResponse:
    if not _dispatcher_instance:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Command dispatcher not initialized",
        )

    if _expected_token and not CommandAuthorizationPolicy.validate_token(token, _expected_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Mattermost verification token",
        )

    payload = SlashCommandPayload(
        channel_id=channel_id,
        channel_name=channel_name,
        command=command,
        response_url=response_url,
        team_id=team_id,
        text=text,
        user_id=user_id,
        user_name=user_name,
        trigger_id=trigger_id,
    )

    return await _dispatcher_instance.dispatch(payload)
