from pydantic import BaseModel


class User(BaseModel):
    id: str  # subject from jwt token (keycloak)
    roles: list[str]
