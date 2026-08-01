from fastapi.testclient import TestClient
from tmmp_smartlead_sync.main import create_app


def test_health_endpoint():
    app = create_app()
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP", "service": "smartlead-sync"}
