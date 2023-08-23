from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.authorization.exceptions import SettingsNotAvailableError
from app.config import Settings
from app.core.models.user import User
from app.rest.settings import get_settings


def decode_jwt(token: str, settings: Settings) -> dict[str, Any]:
    jwks_client = jwt.PyJWKClient(settings.jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(token).key
    decoded_token: dict[str, Any] = jwt.decode(
        jwt=token,
        key=signing_key,
        algorithms=settings.algorithms,
        audience=settings.api_audience,
        issuer=settings.issuer,
    )
    return decoded_token


class JWTBearer:
    def __init__(self) -> None:
        self.http_bearer = HTTPBearer(auto_error=True)
        self.settings: Settings | None = None

    async def __call__(self, settings: Annotated[Settings, Depends(get_settings)], request: Request) -> User:
        self.settings = settings

        if not self.settings.auth_enabled:
            return User(roles=["slas-frontend-user", "test-taker"])

        credentials: HTTPAuthorizationCredentials | None = await self.http_bearer(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme."
                )

            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token or expired token."
                )
            return User(roles=payload["realm_access"]["roles"])

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization code."
        )

    def verify_jwt(self, jwtoken: str) -> dict[str, Any]:
        if not self.settings:
            raise SettingsNotAvailableError()
        try:
            return decode_jwt(jwtoken, self.settings)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc)
            ) from exc
