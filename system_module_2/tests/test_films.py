from fastapi.testclient import TestClient
from system_module_2.server.server import app

client = TestClient(app)


def test_get_film():
    response = client.get("/films/Blacksmith Scene")
    assert response.status_code == 200
    assert "Blacksmith Scene" in response.json().get("summary", "")
