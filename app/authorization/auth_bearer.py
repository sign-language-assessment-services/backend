import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings


def decode_jwt(token: str, settings) -> dict:
    try:
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
        # Try out
        # return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as exc:
        raise exc
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        settings = Settings()
        settings.algorithms = ["RS256"]
        settings.api_audience = "backend"
        settings.auth_enabled = True
        settings.issuer = "http://localhost:9000/auth/realms/slas"
        settings.jwks_url = "http://localhost:9000/auth/realms/slas/protocol/openid-connect/certs"
        self.settings = settings

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwtoken, self.settings)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
