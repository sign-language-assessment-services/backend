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
async def test_jwt_bearer_returns_user(settings: Mock, bearer_credentials: JWTBearer) -> None:
    bearer_credentials.verify_jwt = Mock(  # type: ignore[method-assign]
        return_value={
            "realm_access": {"roles": ["slas-frontend-user", "test-taker"]},
            "sub": "testuser_id"
        }
    )

    result = await bearer_credentials(settings=settings, request=mock.ANY)

    assert result == User(id="testuser_id", roles=["slas-frontend-user", "test-taker"])


@pytest.mark.asyncio
async def test_jwt_bearer_auth_disabled_returns_user(settings: Mock) -> None:
    settings.auth_enabled = False
    bearer = JWTBearer()

    result = await bearer(settings=settings, request=mock.ANY)

    assert result == User(id="anonymous", roles=["slas-frontend-user", "test-taker"])


@pytest.mark.asyncio
async def test_jwt_bearer_no_credentials_raises_unauthorized(settings: Mock, bearer_no_credentials: JWTBearer) -> None:
    with pytest.raises(HTTPException) as exc:
        await bearer_no_credentials(settings=settings, request=mock.ANY)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_jwt_bearer_wrong_scheme_raises_unauthorized(settings: Mock, bearer_wrong_scheme: JWTBearer) -> None:
    with pytest.raises(HTTPException) as exc:
        await bearer_wrong_scheme(settings=settings, request=mock.ANY)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_no_jwt_payload_raises_unauthorized(settings: Mock, bearer_none_credentials: JWTBearer) -> None:
    bearer_none_credentials.verify_jwt = Mock(return_value=None)  # type: ignore[method-assign]

    with pytest.raises(HTTPException) as exc:
        await bearer_none_credentials(settings=settings, request=mock.ANY)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_verify_jwt_no_settings_raises_settings_not_available() -> None:
    bearer = JWTBearer()

    with pytest.raises(SettingsNotAvailableError):
        bearer.verify_jwt("test_token")


@patch("app.authorization.auth_bearer.decode_jwt")
def test_verify_jwt_returns_decoded_token(decoder: Mock, settings: Mock) -> None:
    bearer = JWTBearer()
    bearer.settings = settings
    decoder.return_value = "decoded_token"

    result = bearer.verify_jwt("test_token")

    assert result == "decoded_token"


@patch("app.authorization.auth_bearer.decode_jwt")
def test_verify_jwt_exception_raises_bad_request(decoder: Mock, settings: Mock) -> None:
    bearer = JWTBearer()
    bearer.settings = settings
    decoder.side_effect = Exception()

    with pytest.raises(HTTPException) as exc:
        bearer.verify_jwt("test_token")

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
