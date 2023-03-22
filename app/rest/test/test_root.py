from .base import get_test_client

CLIENT = get_test_client()


def test_get_root() -> None:
    response = CLIENT.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health() -> None:
    response = CLIENT.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
