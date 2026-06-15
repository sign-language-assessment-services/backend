import logging
from typing import Annotated, NoReturn
from uuid import UUID

from fastapi import Depends
from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakConnectionError, KeycloakGetError

from app.external_services.keycloak.dependencies import get_keycloak_admin
from app.services.exceptions.external_service import (
    IdentityProviderUnavailableException, IdentityProviderUnexpectedError
)
from app.services.exceptions.not_found import UserNotFoundException

logger = logging.getLogger(__name__)


class IdentityProviderClient:

    def __init__(self, keycloak_admin: Annotated[KeycloakAdmin, Depends(get_keycloak_admin)]) -> None:
        self.keycloak_admin = keycloak_admin

    async def get_user_info(self, user_id: UUID) -> dict[str, str]:
        try:
            user_data = await self.keycloak_admin.a_get_user(str(user_id))
            logger.debug(
                "Successfully fetched user info for user %(user_id)s",
                {"user_id": user_id},
            )
            return {
                "first_name": user_data.get("firstName", ""),
                "last_name": user_data.get("lastName", ""),
            }
        except KeycloakGetError as exc:
            self._handle_keycloak_get_error(exc, user_id)
        except KeycloakConnectionError as exc:
            self._handle_connection_error(exc)

    async def list_users(self) -> list[dict[str, str]]:
        try:
            user_data = await self.keycloak_admin.a_get_users()
            logger.debug("Successfully fetched users from identity provider")
            return [
                {
                    "uuid": user.get("id"),
                    "username": user.get("username")
                }
                for user in user_data
            ]
        except KeycloakConnectionError as exc:
            self._handle_connection_error(exc)

    async def get_role_names_for_user(self, user_id: UUID) -> set[str]:
        try:
            user_groups = await self.keycloak_admin.a_get_user_groups(str(user_id))
            all_roles = set()
            for group in user_groups:
                user_roles = await self.keycloak_admin.a_get_group_realm_roles(group["id"])
                all_roles.update(role.get("name") for role in user_roles)
            logger.debug(
                "Successfully fetched realm roles from groups for user %(user_id)s",
                {"user_id": user_id},
            )
            return all_roles
        except KeycloakGetError as exc:
            self._handle_keycloak_get_error(exc, user_id)
        except KeycloakConnectionError as exc:
            self._handle_connection_error(exc)

    @staticmethod
    def _handle_connection_error(exc: KeycloakConnectionError) -> NoReturn:
        logger.error("Cannot reach Keycloak: %(exc)s", {"exc": exc})
        raise IdentityProviderUnavailableException("Identity provider is currently unavailable.") from exc

    @staticmethod
    def _handle_keycloak_get_error(exc: KeycloakGetError, user_id: UUID) -> NoReturn:
        if exc.response_code == 404:
            logger.warning("User %(user_id)s not found in Keycloak", {"user_id": user_id})
            raise UserNotFoundException(f"User with id '{user_id}' not found.") from exc

        logger.error(
            "Keycloak returned an error while fetching information for user id '%(user_id)s': %(exc)s",
            {"user_id": user_id, "exc": exc},
        )
        raise IdentityProviderUnexpectedError(
            f"Unexpected identity provider error while fetching information for user id '{user_id}'."
        ) from exc
