from uuid import UUID

from pydantic import BaseModel

from app.core.models.role import UserRole


class GetUserInfoResponse(BaseModel):
    first_name: str
    last_name: str


class ListUsersResponse(BaseModel):
    id: UUID
    username: str
    roles: list[UserRole]
