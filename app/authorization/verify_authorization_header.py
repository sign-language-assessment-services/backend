from typing import Optional

from fastapi_auth_middleware import FastAPIUser
from starlette.authentication import BaseUser
from starlette.datastructures import Headers

from app import settings
from app.authorization.token_verifier import TokenVerifier

token_verifier = TokenVerifier()


def verify_authorization_header(headers: Headers) -> tuple[list[str], Optional[BaseUser]]:
    if not settings.AUTH_ENABLED:
        return (
            ["slas-frontend-user", "test-taker"],
            FastAPIUser(first_name="", last_name="", user_id="")
        )
    if not "authorization" in headers:
        return [], None

    bearer_token = headers["authorization"].removeprefix("Bearer ")
    decoded_access_token = token_verifier.verify(bearer_token)
    scopes = decoded_access_token["realm_access"]["roles"]
    user = FastAPIUser(
        first_name=decoded_access_token["given_name"],
        last_name=decoded_access_token["family_name"],
        user_id=decoded_access_token["sub"]
    )
    return scopes, user
