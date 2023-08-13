from typing import Type
from unittest import mock
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException, status

from app.authorization.auth_bearer import JWTBearer, decode_jwt
from app.authorization.exceptions import SettingsNotAvailableError
from app.core.models.user import User


@patch("app.authorization.auth_bearer.jwt")
def test_decode_jwt(jwt: Mock, jwk_client: Mock, settings: Mock) -> None:
    jwt.PyJWKClient.return_value = jwk_client
    jwt.decode.return_value = "decoded_token"

    result = decode_jwt(token="encoded_token", settings=settings)

    jwk_client.get_signing_key_from_jwt.assert_called_once_with("encoded_token")
    jwt.decode.assert_called_once_with(
        jwt="encoded_token",
        key="signing_key",
        algorithms=mock.ANY,
        audience=mock.ANY,
        issuer=mock.ANY
    )
    assert result == "decoded_token"


@pytest.mark.asyncio
async def test_jwt_bearer_returns_user_if_auth_disabled(settings: Mock) -> None:
    settings.auth_enabled = False
    bearer = JWTBearer()

    result = await bearer(settings=settings, request=mock.ANY)

    assert result == User(roles=["slas-frontend-user", "test-taker"])


@pytest.mark.asyncio
async def test_jwt_bearer_raises_unauthorized_if_no_credentials(settings: Mock) -> None:
    async def http_bearer_return_value() -> None:
        return None

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())

    with pytest.raises(HTTPException) as exc:
        await bearer(settings=settings, request=mock.ANY)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_jwt_bearer_no_credentials_raises_unauthorized(settings: Mock) -> None:
    async def http_bearer_return_value() -> None:
        return None

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())

    with pytest.raises(HTTPException) as exc:
        await bearer(settings=settings, request=mock.ANY)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_jwt_bearer_raises_unauthorized_if_not_bearer_scheme(settings: Mock) -> None:
    class Credentials:
        scheme = "Not-Bearer"

    async def http_bearer_return_value() -> Type[Credentials]:
        return Credentials

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())

    with pytest.raises(HTTPException) as exc:
        await bearer(settings=settings, request=mock.ANY)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_jwt_bearer_wrong_scheme_raises_unauthorized(settings: Mock) -> None:
    class Credentials:
        scheme = "Not-Bearer"

    async def http_bearer_return_value() -> Type[Credentials]:
        return Credentials

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())

    with pytest.raises(HTTPException) as exc:
        await bearer(settings=settings, request=mock.ANY)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_jwt_bearer_raises_unauthorized_if_no_verified_jwt_payload(settings: Mock) -> None:
    class Credentials:
        scheme = "Bearer"
        credentials = None

    async def http_bearer_return_value() -> Type[Credentials]:
        return Credentials

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())
    bearer.verify_jwt = Mock(return_value=None)  # type: ignore[method-assign]

    with pytest.raises(HTTPException) as exc:
        await bearer(settings=settings, request=mock.ANY)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_jwt_bearer_returns_user(settings: Mock) -> None:
    class Credentials:
        scheme = "Bearer"
        credentials = None

    async def http_bearer_return_value() -> Type[Credentials]:
        return Credentials

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())
    bearer.verify_jwt = Mock(  # type: ignore[method-assign]
        return_value={"realm_access": {"roles": ["slas-frontend-user", "test-taker"]}}
    )

    result = await bearer(settings=settings, request=mock.ANY)

    assert result == User(roles=["slas-frontend-user", "test-taker"])


def test_verify_jwt_raises_settings_exception() -> None:
    bearer = JWTBearer()

    with pytest.raises(SettingsNotAvailableError):
        bearer.verify_jwt("test_token")


@patch("app.authorization.auth_bearer.decode_jwt")
def test_verify_jwt_raises_bad_request(decoder: Mock, settings: Mock) -> None:
    bearer = JWTBearer()
    bearer.settings = settings
    decoder.side_effect = Exception()

    with pytest.raises(HTTPException) as exc:
        bearer.verify_jwt("test_token")
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


@patch("app.authorization.auth_bearer.decode_jwt")
def test_verify_jwt_returns_decoded_token(decoder: Mock, settings: Mock) -> None:
    bearer = JWTBearer()
    bearer.settings = settings
    decoder.return_value = "decoded_token"

    result = bearer.verify_jwt("test_token")

    assert result == "decoded_token"
