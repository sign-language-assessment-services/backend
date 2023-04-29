from typing import Any

import jwt

from app import settings


class TokenVerifier:  # pylint: disable=too-few-public-methods
    def __init__(self) -> None:
        self.jwks_client = jwt.PyJWKClient(settings.JWKS_URL)

    def verify(self, token: str) -> dict[str, Any]:
        signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
        return jwt.decode(
            jwt=token,
            key=signing_key,
            algorithms=settings.ALGORITHMS,
            audience=settings.API_AUDIENCE,
            issuer=settings.ISSUER,
        )
