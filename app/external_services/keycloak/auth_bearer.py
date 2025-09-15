import logging
from typing import Annotated, Any
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings
from app.core.models.user import User
from app.external_services.keycloak.exceptions import SettingsNotAvailableError
from app.settings import get_settings

logger = logging.getLogger(__name__)


def decode_jwt(token: str, settings: Settings) -> dict[str, Any]:
    jwks_client = jwt.PyJWKClient(settings.jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(token).key
    logger.debug("Starting decoding JWT token.")
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
            fake_user_id = UUID("00000000-0000-0000-0000-000000000000")
            return User(id=fake_user_id, roles=["slas-frontend-user", "test-taker"])

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
            return User(id=payload["sub"], roles=payload["realm_access"]["roles"])

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization code."
        )

    def verify_jwt(self, jwtoken: str) -> dict[str, Any]:
        if not self.settings:
            raise SettingsNotAvailableError("Settings are not available.")
        try:
            return decode_jwt(jwtoken, self.settings)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc)
            ) from exc
