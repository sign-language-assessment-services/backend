from dataclasses import dataclass, field
from unittest.mock import Mock

import pytest

from app.external_services.keycloak.auth_bearer import JWTBearer


@dataclass
class Credentials:
    scheme: str | None = field(default="Bearer")
    credentials: str | None = field(default=None)


class JwtSigningKey:
    key = "signing_key"


@pytest.fixture
def jwk_client() -> Mock:
    jwks_client = Mock()
    jwks_client.get_signing_key_from_jwt.return_value = JwtSigningKey
    return jwks_client


@pytest.fixture
def bearer_credentials() -> JWTBearer:
    async def http_bearer_return_value() -> Credentials:
        return Credentials(credentials="test_credentials")

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())
    return bearer


@pytest.fixture
def bearer_no_credentials() -> JWTBearer:
    async def http_bearer_return_value() -> None:
        return None

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())
    return bearer


@pytest.fixture
def bearer_none_credentials() -> JWTBearer:
    async def http_bearer_return_value() -> Credentials:
        return Credentials()

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())
    return bearer


@pytest.fixture
def bearer_wrong_scheme() -> JWTBearer:
    async def http_bearer_return_value() -> Credentials:
        return Credentials(scheme="Not-Bearer")

    bearer = JWTBearer()
    bearer.http_bearer = Mock(return_value=http_bearer_return_value())
    return bearer
