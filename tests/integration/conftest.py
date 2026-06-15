import pytest
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection

from app.external_services.keycloak.client import IdentityProviderClient
from tests.integration.helper import SETTINGS


@pytest.fixture
def real_keycloak_admin() -> KeycloakAdmin:
    """Credentials from TestSettings and .testenv file"""
    connection = KeycloakOpenIDConnection(
        server_url=SETTINGS.keycloak_server_url,
        realm_name=SETTINGS.keycloak_realm,
        client_id=SETTINGS.client_id,
        client_secret_key=SETTINGS.client_secret,
        verify=True,
    )
    return KeycloakAdmin(connection=connection)


@pytest.fixture
def real_identity_provider_client(real_keycloak_admin: KeycloakAdmin) -> IdentityProviderClient:
    return IdentityProviderClient(keycloak_admin=real_keycloak_admin)
