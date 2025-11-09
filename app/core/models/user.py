from uuid import UUID

from pydantic import BaseModel

from app.core.models.role import UserRole


class User(BaseModel):
    id: UUID  # subject from jwt token (keycloak)
    roles: list[UserRole]
