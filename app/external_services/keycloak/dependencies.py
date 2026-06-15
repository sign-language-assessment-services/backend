import logging
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection

from app.config import Settings
from app.settings import get_settings

logger = logging.getLogger(__name__)


@lru_cache()
def get_keycloak_admin(settings: Annotated[Settings, Depends(get_settings)]) -> KeycloakAdmin:
    """Create and return a process-wide "singleton" KeycloakAdmin instance.

    Token lifecycle (fetch, refresh, 401-retry) is fully managed by the
    python-keycloak library via KeycloakOpenIDConnection.
    """
    logger.info(
        "Initializing KeycloakAdmin for realm %(realm)s at %(server_url)s",
        {"realm": settings.keycloak_realm, "server_url": settings.keycloak_server_url},
    )
    connection = KeycloakOpenIDConnection(
        server_url=settings.keycloak_server_url,
        realm_name=settings.keycloak_realm,
        client_id=settings.client_id,
        client_secret_key=settings.client_secret,
        verify=True,
    )
    return KeycloakAdmin(connection=connection)
