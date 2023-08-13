from unittest.mock import Mock

import pytest


@pytest.fixture
def jwk_client() -> Mock:
    jwks_client = Mock()

    class JwtSigningKey:
        key = "signing_key"

    jwks_client.get_signing_key_from_jwt.return_value = JwtSigningKey
    return jwks_client
