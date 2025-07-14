from fastapi.testclient import TestClient
from system_module_2.server.server import app

client = TestClient(app)


def test_get_person():
    response = client.get("/people/Bruce Lee")
    assert response.status_code == 200
    assert "Bruce Lee" in response.json().get("summary", "")


