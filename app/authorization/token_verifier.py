import os

import jwt


class TokenVerifier:
    def __init__(self):
        self.config = self.set_up()
        self.jwks_client = jwt.PyJWKClient(self.config["JWKS_URL"])

    def set_up(self):
        return {
            "JWKS_URL": os.getenv("JWKS_URL"),
            "API_AUDIENCE": os.getenv("API_AUDIENCE"),
            "ISSUER": os.getenv("ISSUER"),
            "ALGORITHMS": os.getenv("ALGORITHMS"),
        }

    def verify(self, token):
        signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
        return jwt.decode(
            token,
            signing_key,
            algorithms=self.config["ALGORITHMS"],
            audience=self.config["API_AUDIENCE"],
            issuer=self.config["ISSUER"],
        )
