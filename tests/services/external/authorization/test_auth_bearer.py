from unittest import mock
from unittest.mock import Mock, patch
from uuid import UUID

import pytest
from fastapi import HTTPException, status

import app.external_services.keycloak.auth_bearer as auth_bearer_module
from app.core.models.role import UserRole
from app.core.models.user import User
from app.external_services.keycloak.auth_bearer import JWTBearer, decode_jwt
from tests.data.models.users import test_taker_1
from tests.settings_for_tests import TestSettings


@patch.object(auth_bearer_module, auth_bearer_module.jwt.__name__)
def test_decode_jwt(jwt: Mock, jwk_client: Mock) -> None:
    jwt.PyJWKClient.return_value = jwk_client
    jwt.decode.return_value = {"token": "decoded_token"}

    result = decode_jwt(token="encoded_token", settings=Mock())

    jwk_client.get_signing_key_from_jwt.assert_called_once_with("encoded_token")
    jwt.decode.assert_called_once_with(
        jwt="encoded_token",
        key="signing_key",
        algorithms=mock.ANY,
        audience=mock.ANY,
        issuer=mock.ANY
    )
    assert result == {"token": "decoded_token"}


@pytest.mark.asyncio
async def test_jwt_bearer_returns_user(settings: TestSettings, bearer_credentials: JWTBearer) -> None:
    settings.auth_enabled = True
    bearer_credentials.verify_jwt = Mock(  # type: ignore[method-assign]
        return_value={
            "realm_access": {"roles": test_taker_1.roles},
            "sub": str(test_taker_1.id)
        }
    )

    result = await bearer_credentials(settings=settings, request=mock.ANY)

    assert result == User(id=test_taker_1.id, roles=test_taker_1.roles)


@pytest.mark.asyncio
async def test_jwt_bearer_auth_disabled_returns_user(settings: TestSettings) -> None:
    settings.auth_enabled = False
    bearer = JWTBearer()

    result = await bearer(settings=settings, request=mock.ANY)

    fake_user_id = UUID("00000000-0000-0000-0000-000000000000")
    assert result == User(id=fake_user_id, roles=[UserRole.FRONTEND, UserRole.TEST_TAKER])


@pytest.mark.asyncio
async def test_jwt_bearer_no_credentials_raises_unauthorized(bearer_no_credentials: JWTBearer) -> None:
    with pytest.raises(HTTPException) as exc:
        await bearer_no_credentials(settings=Mock(), request=mock.ANY)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_jwt_bearer_wrong_scheme_raises_unauthorized(bearer_wrong_scheme: JWTBearer) -> None:
    with pytest.raises(HTTPException) as exc:
        await bearer_wrong_scheme(settings=Mock(), request=mock.ANY)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_no_jwt_payload_raises_unauthorized(bearer_none_credentials: JWTBearer) -> None:
    bearer_none_credentials.verify_jwt = Mock(return_value=None)  # type: ignore[method-assign]

    with pytest.raises(HTTPException) as exc:
        await bearer_none_credentials(settings=Mock(), request=mock.ANY)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@patch.object(auth_bearer_module, decode_jwt.__name__)
def test_verify_jwt_returns_decoded_token(decoder: Mock, settings: TestSettings) -> None:
    bearer = JWTBearer()
    decoder.return_value = {"token": "decoded_token"}

    result = bearer.verify_jwt("test_token")

    assert result == {"token": "decoded_token"}


@patch.object(auth_bearer_module, decode_jwt.__name__)
def test_verify_jwt_exception_raises_bad_request(decoder: Mock, settings: TestSettings) -> None:
    bearer = JWTBearer()
    decoder.side_effect = Exception()

    with pytest.raises(HTTPException) as exc:
        bearer.verify_jwt("test_token")

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
