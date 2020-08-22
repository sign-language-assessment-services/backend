from .base import get_test_client

CLIENT = get_test_client()


def test_get_root():
    response = CLIENT.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World!"}
