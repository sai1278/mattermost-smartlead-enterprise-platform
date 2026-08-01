from tmmp_command_handler.domain.authorization import CommandAuthorizationPolicy
from tmmp_command_handler.domain.commands import WarmupListCommand, WarmupStatusCommand


def test_authorization_policy():
    assert CommandAuthorizationPolicy.validate_token("token123", "token123") is True
    assert CommandAuthorizationPolicy.validate_token("token123", "wrong") is False
    assert CommandAuthorizationPolicy.validate_token("", "token123") is False


def test_command_dataclasses():
    cmd = WarmupStatusCommand(
        user_id="u1",
        user_name="alice",
        channel_id="c1",
        team_id="t1",
        mailbox="101",
    )
    assert cmd.user_id == "u1"
    assert cmd.mailbox == "101"

    cmd_list = WarmupListCommand(user_id="u1", user_name="alice", channel_id="c1", team_id="t1")
    assert cmd_list.user_name == "alice"
