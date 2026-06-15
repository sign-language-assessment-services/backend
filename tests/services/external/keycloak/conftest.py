from unittest.mock import AsyncMock, create_autospec
from uuid import UUID

import pytest
from keycloak import KeycloakAdmin

from app.external_services.keycloak.client import IdentityProviderClient


@pytest.fixture
def mock_keycloak_admin() -> AsyncMock:
    return create_autospec(KeycloakAdmin, instance=True)


@pytest.fixture
def identity_provider_client(mock_keycloak_admin: AsyncMock) -> IdentityProviderClient:
    return IdentityProviderClient(keycloak_admin=mock_keycloak_admin)


@pytest.fixture
def test_user_id() -> UUID:
    return UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def keycloak_user_response() -> dict:
    return {
        "id": "12345678-1234-5678-1234-567812345678",
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "enabled": True,
    }
