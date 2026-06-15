from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from keycloak.exceptions import KeycloakConnectionError, KeycloakGetError

from app.external_services.keycloak.client import IdentityProviderClient
from app.services.exceptions.external_service import (
    IdentityProviderUnavailableException, IdentityProviderUnexpectedError
)
from app.services.exceptions.not_found import UserNotFoundException


@pytest.mark.asyncio
async def test_get_user_info_returns_first_and_last_name(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
    keycloak_user_response: dict,
) -> None:
    mock_keycloak_admin.a_get_user.return_value = keycloak_user_response

    result = await identity_provider_client.get_user_info(test_user_id)

    assert result == {"first_name": "John", "last_name": "Doe"}
    mock_keycloak_admin.a_get_user.assert_called_once_with(str(test_user_id))


@pytest.mark.asyncio
async def test_get_user_info_returns_empty_strings_when_names_missing(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user.return_value = {
        "id": str(test_user_id),
        "username": "johndoe",
    }

    result = await identity_provider_client.get_user_info(test_user_id)

    assert result == {"first_name": "", "last_name": ""}


@pytest.mark.asyncio
async def test_get_user_info_raises_user_not_found_on_404(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user.side_effect = KeycloakGetError(
        error_message="User not found",
        response_code=404,
        response_body=b"",
    )

    with pytest.raises(UserNotFoundException) as exc_info:
        await identity_provider_client.get_user_info(test_user_id)

    assert str(test_user_id) in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_user_info_raises_unavailable_on_non_404_keycloak_error(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user.side_effect = KeycloakGetError(
        error_message="Internal Server Error",
        response_code=500,
        response_body=b"",
    )

    with pytest.raises(IdentityProviderUnexpectedError):
        await identity_provider_client.get_user_info(test_user_id)


@pytest.mark.asyncio
async def test_get_user_info_raises_unavailable_on_connection_error(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user.side_effect = KeycloakConnectionError(
        error_message="Connection refused",
    )

    with pytest.raises(IdentityProviderUnavailableException):
        await identity_provider_client.get_user_info(test_user_id)


@pytest.mark.asyncio
async def test_get_role_names_for_user_returns_roles_from_groups(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user_groups.return_value = [
        {"id": "group-1", "name": "teachers"},
        {"id": "group-2", "name": "admins"},
    ]
    mock_keycloak_admin.a_get_group_realm_roles.side_effect = [
        [{"id": "role-1", "name": "test-scorer"}, {"id": "role-2", "name": "slas-frontend-user"}],
        [{"id": "role-3", "name": "realm-admin"}],
    ]

    result = await identity_provider_client.get_role_names_for_user(test_user_id)

    assert result == {"test-scorer", "slas-frontend-user", "realm-admin"}
    mock_keycloak_admin.a_get_user_groups.assert_called_once_with(str(test_user_id))


@pytest.mark.asyncio
async def test_get_role_names_for_user_returns_empty_set_when_no_groups(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user_groups.return_value = []

    result = await identity_provider_client.get_role_names_for_user(test_user_id)

    assert result == set()
    mock_keycloak_admin.a_get_group_realm_roles.assert_not_called()


@pytest.mark.asyncio
async def test_get_role_names_for_user_returns_unique_roles(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user_groups.return_value = [
        {"id": "group-1", "name": "teachers"},
        {"id": "group-2", "name": "admins"},
    ]
    mock_keycloak_admin.a_get_group_realm_roles.side_effect = [
        [{"id": "role-1", "name": "test-scorer"}, {"id": "role-2", "name": "shared-role"}],
        [{"id": "role-3", "name": "shared-role"}],  # Duplicate role
    ]

    result = await identity_provider_client.get_role_names_for_user(test_user_id)

    assert result == {"test-scorer", "shared-role"}


@pytest.mark.asyncio
async def test_get_role_names_for_user_raises_user_not_found_on_404(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user_groups.side_effect = KeycloakGetError(
        error_message="User not found",
        response_code=404,
        response_body=b"",
    )

    with pytest.raises(UserNotFoundException) as exc_info:
        await identity_provider_client.get_role_names_for_user(test_user_id)

    assert str(test_user_id) in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_role_names_for_user_raises_unavailable_on_non_404_keycloak_error(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user_groups.side_effect = KeycloakGetError(
        error_message="Internal Server Error",
        response_code=500,
        response_body=b"",
    )

    with pytest.raises(IdentityProviderUnexpectedError):
        await identity_provider_client.get_role_names_for_user(test_user_id)


@pytest.mark.asyncio
async def test_get_role_names_for_user_raises_unavailable_on_connection_error(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_keycloak_admin.a_get_user_groups.side_effect = KeycloakConnectionError(
        error_message="Connection refused",
    )

    with pytest.raises(IdentityProviderUnavailableException):
        await identity_provider_client.get_role_names_for_user(test_user_id)


@pytest.mark.asyncio
async def test_list_users_returns_users_without_roles(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
) -> None:
    user_id_1 = UUID("11111111-1111-1111-1111-111111111111")
    user_id_2 = UUID("22222222-2222-2222-2222-222222222222")
    mock_keycloak_admin.a_get_users.return_value = [
        {"id": str(user_id_1), "username": "theo@a.de"},
        {"id": str(user_id_2), "username": "lena@a.de"},
    ]

    result = await identity_provider_client.list_users()

    assert len(result) == 2
    assert result[0]["uuid"] == str(user_id_1)
    assert result[0]["username"] == "theo@a.de"
    assert result[1]["uuid"] == str(user_id_2)
    assert result[1]["username"] == "lena@a.de"


@pytest.mark.asyncio
async def test_list_users_returns_empty_list_when_no_users_exist(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
) -> None:
    mock_keycloak_admin.a_get_users.return_value = []

    result = await identity_provider_client.list_users()

    assert result == []


@pytest.mark.asyncio
async def test_list_users_raises_unavailable_on_connection_error(
    identity_provider_client: IdentityProviderClient,
    mock_keycloak_admin: AsyncMock,
) -> None:
    mock_keycloak_admin.a_get_users.side_effect = KeycloakConnectionError(
        error_message="Connection refused",
    )

    with pytest.raises(IdentityProviderUnavailableException):
        await identity_provider_client.list_users()
