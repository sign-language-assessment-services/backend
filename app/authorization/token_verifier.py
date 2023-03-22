import os
from typing import Any

import jwt


class TokenVerifier:
    def __init__(self) -> None:
        self.config = self.set_up()
        self.jwks_client = jwt.PyJWKClient(self.config["JWKS_URL"])

    @staticmethod
    def set_up() -> dict[str, str]:
        mandatory_keys = {"JWKS_URL", "API_AUDIENCE", "ISSUER", "ALGORITHMS"}
        config = {}
        for key in mandatory_keys:
            value = os.getenv(key)
            if not value:
                raise EnvironmentError(f"Missing env variable {key}.")
            config[key] = value
        return config

    def verify(self, token: str) -> dict[str, Any]:
        signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
        return jwt.decode(
            token,
            signing_key,
            algorithms=[self.config["ALGORITHMS"]],
            audience=self.config["API_AUDIENCE"],
            issuer=self.config["ISSUER"],
        )
