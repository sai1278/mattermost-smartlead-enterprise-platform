from tmmp_integrations_mattermost.dto import (
    ChannelDTO,
    PostDTO,
    SlashCommandPayload,
    SlashCommandResponse,
    UserDTO,
)


def test_user_dto():
    u = UserDTO(id="u1", username="john_doe", email="john@example.com")
    assert u.id == "u1"
    assert u.username == "john_doe"


def test_channel_dto():
    c = ChannelDTO(id="c1", team_id="t1", type="O", name="general")
    assert c.id == "c1"
    assert c.name == "general"


def test_post_dto():
    p = PostDTO(id="p1", channel_id="c1", user_id="u1", message="hello world")
    assert p.id == "p1"
    assert p.message == "hello world"


def test_slash_command_payload_and_response():
    payload = SlashCommandPayload(
        channel_id="c1",
        channel_name="town-square",
        command="/warmup",
        response_url="http://localhost/resp",
        team_id="t1",
        text="status",
        user_id="u1",
        user_name="admin",
    )
    assert payload.command == "/warmup"

    resp = SlashCommandResponse(response_type="ephemeral", text="Processing request...")
    assert resp.response_type == "ephemeral"
    assert resp.text == "Processing request..."
