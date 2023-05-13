from typing import Any, Annotated, Optional

import jwt
from fastapi import Depends
from fastapi_auth_middleware import FastAPIUser
from starlette.authentication import BaseUser

from app.config import Settings
from app.rest.settings2 import get_settings


class TokenVerifier:  # pylint: disable=too-few-public-methods
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]) -> None:
        self.settings = settings
        self.jwks_client = jwt.PyJWKClient(self.settings.jwks_url)

    def verify_authorization_header(self, auth_header: str) -> tuple[list[str], Optional[BaseUser]]:
        if not self.settings.auth_enabled:
            return (
                ["slas-frontend-user", "test-taker"],
                FastAPIUser(first_name="", last_name="", user_id="")
            )

        bearer_token = auth_header.removeprefix("Bearer ")
        decoded_access_token = self.verify(bearer_token)
        scopes = decoded_access_token["realm_access"]["roles"]
        user = FastAPIUser(
            first_name=decoded_access_token["given_name"],
            last_name=decoded_access_token["family_name"],
            user_id=decoded_access_token["sub"]
        )
        return scopes, user

    def verify(self, token: str) -> dict[str, Any]:
        signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
        return jwt.decode(
            jwt=token,
            key=signing_key,
            algorithms=self.settings.algorithms,
            audience=self.settings.api_audience,
            issuer=self.settings.issuer,
        )
