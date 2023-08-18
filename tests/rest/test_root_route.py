import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("endpoint", ["/", "/health"])
def test_health_endpoint_returns_status_ok(endpoint: str, test_client: TestClient) -> None:
    response = test_client.get(endpoint)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
