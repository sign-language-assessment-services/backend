from fastapi.testclient import TestClient


def test_get_root(test_client: TestClient) -> None:
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health(test_client: TestClient) -> None:
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
