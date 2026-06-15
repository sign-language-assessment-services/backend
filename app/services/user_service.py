import asyncio
import logging
from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.core.models.role import UserRole
from app.core.models.user import User, UserInfo
from app.external_services.keycloak.client import IdentityProviderClient

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, identity_provider_client: Annotated[IdentityProviderClient, Depends()]) -> None:
        self.identity_provider_client = identity_provider_client

    async def get_user_info_by_id(self, user_id: UUID) -> UserInfo:
        logger.debug("Fetching user info for user %(user_id)s", {"user_id": user_id})
        user_info = await self.identity_provider_client.get_user_info(user_id=user_id)
        return UserInfo(**user_info)

    async def list_users(self) -> list[User]:
        logger.debug("Fetching all users from identity provider")
        users = await self.identity_provider_client.list_users()
        parallel_async_role_tasks = [
            self.identity_provider_client.get_role_names_for_user(UUID(user["uuid"]))
            for user in users
        ]
        all_roles = await asyncio.gather(*parallel_async_role_tasks)
        return [
            User(
                id=UUID(user["uuid"]),
                username=user["username"],
                roles=[
                    UserRole(role_name) for role_name in roles
                ]
            )
            for user, roles in zip(users, all_roles)
        ]
