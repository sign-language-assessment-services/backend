from uuid import UUID

from pydantic import BaseModel, Field

from app.core.models.role import UserRole


class User(BaseModel):
    id: UUID  # subject from jwt token (keycloak)
    username: str | None = Field(
        default=None,
        description="Username from Identity Provider"
    )
    roles: list[UserRole]


class UserInfo(BaseModel):
    first_name: str
    last_name: str
