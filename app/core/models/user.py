from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID  # subject from jwt token (keycloak)
    roles: list[str]
