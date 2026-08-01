from tmmp_integrations_mattermost.websocket import (
    MattermostWebSocketClient,
    MattermostWebSocketEvent,
)


def test_websocket_event_parsing():
    raw_data = {
        "event": "posted",
        "data": {"post": '{"id": "p1", "message": "test"}'},
        "seq": 10,
    }
    event = MattermostWebSocketEvent(raw_data)
    assert event.event == "posted"
    assert event.seq == 10
    assert "post" in event.data


def test_websocket_client_init():
    client = MattermostWebSocketClient(ws_url="http://localhost:8065", bot_token="token-123")
    assert client.ws_url == "http://localhost:8065/api/v4/websocket"
