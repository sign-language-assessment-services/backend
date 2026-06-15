from uuid import UUID

from fastapi import status
from fastapi.testclient import TestClient

from tests.data.models.users import test_scorer_1, test_taker_1

TESTUSER_ID = UUID("12345678-1234-5678-1234-567812345678")


def test_get_user_info_returns_200_with_user_info(test_client_with_scorer_role: TestClient) -> None:
    response = test_client_with_scorer_role.get(f"/users/{TESTUSER_ID}")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["first_name"] == "John"
    assert body["last_name"] == "Doe"


def test_get_user_info_returns_403_for_non_scorer(test_client: TestClient) -> None:
    response = test_client.get(f"/users/{TESTUSER_ID}")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_info_returns_503_when_identity_provider_unavailable(test_client_with_user_service_unavailable: TestClient) -> None:
    response = test_client_with_user_service_unavailable.get(f"/users/{TESTUSER_ID}")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "unavailable" in response.json()["detail"]


def test_list_users_returns_200_with_users(test_client_with_scorer_role: TestClient) -> None:
    response = test_client_with_scorer_role.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body) == 2
    assert body[0]["username"] == test_scorer_1.username
    assert set(body[0]["roles"]) == {role.value for role in test_scorer_1.roles}
    assert body[1]["username"] == test_taker_1.username
    assert set(body[1]["roles"]) == {role.value for role in test_taker_1.roles}


def test_list_users_returns_403_for_non_scorer(test_client: TestClient) -> None:
    response = test_client.get("/users/")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_users_returns_503_when_identity_provider_unavailable(test_client_with_user_service_unavailable: TestClient) -> None:
    response = test_client_with_user_service_unavailable.get("/users/")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "unavailable" in response.json()["detail"]
