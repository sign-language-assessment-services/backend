import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("endpoint", ["/", "/health"])
def test_health_endpoint_returns_status_ok(endpoint: str, test_client: TestClient) -> None:
    response = test_client.get(endpoint)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_limiter_rejects_too_many_requests(test_client: TestClient) -> None:
    error_msg = "Too many requests: Only 30 requests per minutes are allowed."
    for i in range(100):
        response = test_client.get("/")
        if i >= 30:
            assert response.status_code == 429
            assert response.json() == {"detail": error_msg}
