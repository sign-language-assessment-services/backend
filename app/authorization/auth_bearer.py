from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings
from app.core.models.user import User
from app.rest.settings import get_settings


def decode_jwt(token: str, settings) -> dict:
    jwks_client = jwt.PyJWKClient(settings.jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(token).key
    decoded_token = jwt.decode(
        jwt=token,
        key=signing_key,
        algorithms=settings.algorithms,
        audience=settings.api_audience,
        issuer=settings.issuer,
    )
    return decoded_token


class JWTBearer:
    def __init__(self):
        self.http_bearer = HTTPBearer(auto_error=True)

    async def __call__(self, settings: Annotated[Settings, Depends(get_settings)], request: Request):
        self.settings = settings

        if not self.settings.auth_enabled:
            return User(roles=["slas-frontend-user", "test-taker"])

        credentials: HTTPAuthorizationCredentials = await self.http_bearer(request)
        if credentials:
            if not credentials.scheme == "Bearer":
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

    def verify_jwt(self, jwtoken: str) -> dict:
        try:
            return decode_jwt(jwtoken, self.settings)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc)
            ) from exc
