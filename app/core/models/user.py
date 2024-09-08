from pydantic import BaseModel

from app.type_hints import UserRoles


class User(BaseModel):
    id: str  # subject from jwt token (keycloak)
    roles: UserRoles
