"""User roles for authorization

The purpose of this module is to map the user roles, which are
necessary for implementing the authorization logic. The roles should be
aligned with the roles defined in an external identity provider. We are
using Keycloak for this. (https://www.keycloak.org/)

The application code does not introduce roles by itself, meaning it
also does not read roles from a database or save roles anywhere. The
roles are purely coming in as an detail in so-called jwt tokens.

In this case we are looking at
{
    ...
    "realm_access": {
        "roles": [
            "slas-frontend-user",
            "test-taker",
            ...
        ]
    },
    ...
}
"""

from enum import StrEnum


class UserRole(StrEnum):
    """The user roles are defined in Keycloak realm slas"""
    # Keycloak specific roles
    DEFAULT = "default-roles-slas"
    UMA_AUTHORIZATION = "uma_authorization"
    OFFLINE = "offline_access"

    # These are the roles used for application authorization, and
    # should be used in application code.
    FRONTEND = "slas-frontend-user"
    TEST_SCORER = "test-scorer"
    TEST_TAKER = "test-taker"
