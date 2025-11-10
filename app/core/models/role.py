from enum import StrEnum


class UserRole(StrEnum):
    """The user roles are defined in Keycloak realm slas"""
    DEFAULT = "default-roles-slas"
    FRONTEND = "slas-frontend-user"
    TEST_SCORER = "test-scorer"
    TEST_TAKER = "test-taker"
    UMA_AUTHORIZATION = "uma_authorization"
    OFFLINE = "offline_access"
