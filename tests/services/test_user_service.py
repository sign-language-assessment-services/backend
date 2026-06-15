from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from services.conftest import mock_identity_provider_client, test_user_id, user_service

from app.core.models.role import UserRole
from app.core.models.user import UserInfo
from app.services.exceptions.external_service import IdentityProviderUnavailableException
from app.services.exceptions.not_found import UserNotFoundException
from app.services.user_service import UserService


@pytest.mark.asyncio
async def test_get_user_info_by_id_returns_user_info(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_identity_provider_client.get_user_info.return_value = {"first_name": "John", "last_name": "Doe"}

    result = await user_service.get_user_info_by_id(test_user_id)

    assert isinstance(result, UserInfo)
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    mock_identity_provider_client.get_user_info.assert_called_once_with(user_id=test_user_id)


@pytest.mark.asyncio
async def test_get_user_info_by_id_with_special_characters(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_identity_provider_client.get_user_info.return_value = {"first_name": "François", "last_name": "Müller"}

    result = await user_service.get_user_info_by_id(test_user_id)

    assert result.first_name == "François"
    assert result.last_name == "Müller"


@pytest.mark.asyncio
async def test_get_user_info_by_id_propagates_user_not_found(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_identity_provider_client.get_user_info.side_effect = UserNotFoundException(
        f"User with id '{test_user_id}' not found."
    )

    with pytest.raises(UserNotFoundException) as exc_info:
        await user_service.get_user_info_by_id(test_user_id)

    assert str(test_user_id) in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_user_info_by_id_propagates_identity_provider_unavailable(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_identity_provider_client.get_user_info.side_effect = IdentityProviderUnavailableException(
        "Identity provider is currently unavailable."
    )

    with pytest.raises(IdentityProviderUnavailableException):
        await user_service.get_user_info_by_id(test_user_id)


@pytest.mark.asyncio
async def test_get_user_info_by_id_returns_user_info_model(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_identity_provider_client.get_user_info.return_value = {"first_name": "Jane", "last_name": "Smith"}

    result = await user_service.get_user_info_by_id(test_user_id)

    assert isinstance(result, UserInfo)
    assert result.model_dump() == {"first_name": "Jane", "last_name": "Smith"}


@pytest.mark.asyncio
async def test_get_user_info_by_id_with_empty_names(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
    test_user_id: UUID,
) -> None:
    mock_identity_provider_client.get_user_info.return_value = {"first_name": "", "last_name": ""}

    result = await user_service.get_user_info_by_id(test_user_id)

    assert result.first_name == ""
    assert result.last_name == ""


@pytest.mark.asyncio
async def test_list_users_returns_users_with_roles(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
) -> None:
    user_id_1 = UUID("11111111-1111-1111-1111-111111111111")
    user_id_2 = UUID("22222222-2222-2222-2222-222222222222")
    
    mock_identity_provider_client.list_users.return_value = [
        {"uuid": str(user_id_1), "username": "theo@a.de"},
        {"uuid": str(user_id_2), "username": "lena@a.de"},
    ]
    mock_identity_provider_client.get_role_names_for_user.side_effect = [
        {"test-scorer", "slas-frontend-user"},
        {"test-taker", "slas-frontend-user"},
    ]

    result = await user_service.list_users()

    assert len(result) == 2
    assert result[0].id == user_id_1
    assert result[0].username == "theo@a.de"
    assert set(r.value for r in result[0].roles) == {"test-scorer", "slas-frontend-user"}
    assert result[1].id == user_id_2
    assert result[1].username == "lena@a.de"
    assert set(r.value for r in result[1].roles) == {"test-taker", "slas-frontend-user"}


@pytest.mark.asyncio
async def test_list_users_returns_empty_list_when_no_users(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
) -> None:
    mock_identity_provider_client.list_users.return_value = []

    result = await user_service.list_users()

    assert result == []
    mock_identity_provider_client.get_role_names_for_user.assert_not_called()


@pytest.mark.asyncio
async def test_list_users_returns_users_with_empty_roles(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
) -> None:
    user_id = UUID("33333333-3333-3333-3333-333333333333")
    mock_identity_provider_client.list_users.return_value = [{"uuid": str(user_id), "username": "ned@a.de"}]
    mock_identity_provider_client.get_role_names_for_user.return_value = set()

    result = await user_service.list_users()

    assert len(result) == 1
    assert result[0].id == user_id
    assert result[0].username == "ned@a.de"
    assert result[0].roles == []


@pytest.mark.asyncio
async def test_list_users_propagates_exception_from_get_role_names_for_user(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
) -> None:
    user_id = UUID("44444444-4444-4444-4444-444444444444")
    mock_identity_provider_client.list_users.return_value = [{"uuid": str(user_id), "username": "user@a.de"}]
    mock_identity_provider_client.get_role_names_for_user.side_effect = IdentityProviderUnavailableException(
        "Identity provider is currently unavailable."
    )

    with pytest.raises(IdentityProviderUnavailableException):
        await user_service.list_users()


@pytest.mark.asyncio
async def test_list_users_uses_asyncio_gather_for_parallel_execution(
    user_service: UserService,
    mock_identity_provider_client: AsyncMock,
) -> None:
    user_id_1 = UUID("55555555-5555-5555-5555-555555555555")
    user_id_2 = UUID("66666666-6666-6666-6666-666666666666")
    user_id_3 = UUID("77777777-7777-7777-7777-777777777777")
    mock_identity_provider_client.list_users.return_value = [
        {"uuid": str(user_id_1), "username": "user1@a.de"},
        {"uuid": str(user_id_2), "username": "user2@a.de"},
        {"uuid": str(user_id_3), "username": "user3@a.de"},
    ]
    mock_identity_provider_client.get_role_names_for_user.side_effect = [
        {"test-scorer"},
        {"test-taker"},
        {"slas-frontend-user"},
    ]

    result = await user_service.list_users()

    assert mock_identity_provider_client.get_role_names_for_user.call_count == 3
    assert len(result) == 3
    assert result[0].id == user_id_1
    assert result[0].username == "user1@a.de"
    assert result[0].roles == [UserRole.TEST_SCORER]
    assert result[1].id == user_id_2
    assert result[1].username == "user2@a.de"
    assert result[1].roles == [UserRole.TEST_TAKER]
    assert result[2].id == user_id_3
    assert result[2].username == "user3@a.de"
    assert result[2].roles == [UserRole.FRONTEND]
