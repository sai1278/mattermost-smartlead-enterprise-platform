from fastapi.testclient import TestClient
from tmmp_mattermost_bot.main import create_app


def test_bot_health_endpoint():
    app = create_app()
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "mattermost-bot"
