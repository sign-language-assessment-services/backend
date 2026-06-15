from uuid import UUID

import pytest
from keycloak import KeycloakAdmin

from app.external_services.keycloak.client import IdentityProviderClient
from tests.integration.helper import SETTINGS, THEO_USERNAME, _keycloak_is_reachable


@pytest.mark.skipif(
    # TODO: create integration test runs for local and CI/CD
    #       - with skipif test can be run together with unit tests.
    #       - If we have a running keycloak, this test should pass.
    #       - After configuring integration tests, delete skipif.
    not _keycloak_is_reachable(),
    reason=f"Keycloak not reachable at {SETTINGS.keycloak_server_url}"
)
@pytest.mark.asyncio
async def test_backend_service_account_can_fetch_theo_teacher(
    real_keycloak_admin: KeycloakAdmin,
    real_identity_provider_client: IdentityProviderClient,
) -> None:
    users = await real_keycloak_admin.a_get_users({"username": THEO_USERNAME})
    theo_id = UUID(users[0]["id"])

    result = await real_identity_provider_client.get_user_info(theo_id)

    assert len(users) == 1
    assert result["first_name"] == "Theo"
    assert result["last_name"] == "Teacher"
