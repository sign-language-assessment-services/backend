class ExternalServiceException(Exception):
    """Base class for all external service exceptions."""
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "External service error.")


class IdentityProviderUnavailableException(ExternalServiceException):
    """Raised when the identity provider (Keycloak) is unavailable."""


class IdentityProviderUnexpectedError(ExternalServiceException):
    """Raised on unexpected errors while calling identity provider (Keycloak)."""
