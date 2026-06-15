from unittest.mock import MagicMock, patch

from keycloak import KeycloakAdmin, KeycloakOpenIDConnection

from app.external_services.keycloak import dependencies
from app.external_services.keycloak.dependencies import get_keycloak_admin


@patch.object(dependencies, KeycloakOpenIDConnection.__name__)
@patch.object(dependencies, KeycloakAdmin.__name__)
def test_get_keycloak_admin_returns_keycloak_admin_instance(mock_admin_class: MagicMock, _: MagicMock) -> None:
    mock_settings = MagicMock()
    mock_settings.keycloak_server_url = "http://localhost:9000/auth/"
    mock_settings.keycloak_realm = "slas"
    mock_settings.client_id = "test_client"
    mock_settings.client_secret = "test_secret"
    mock_admin_instance = MagicMock()
    mock_admin_class.return_value = mock_admin_instance

    result = get_keycloak_admin(mock_settings)

    mock_admin_class.assert_called_once()
    assert result is mock_admin_instance


@patch.object(dependencies, KeycloakOpenIDConnection.__name__)
@patch.object(dependencies, KeycloakAdmin.__name__)
def test_get_keycloak_admin_is_singleton_via_lru_cache(mock_admin_class: MagicMock, _: MagicMock) -> None:
    mock_settings = MagicMock()
    mock_settings.keycloak_server_url = "http://localhost:9000/auth/"
    mock_settings.keycloak_realm = "slas"
    mock_settings.client_id = "test_client"
    mock_settings.client_secret = "test_secret"
    mock_admin_instance = MagicMock()
    mock_admin_class.return_value = mock_admin_instance

    first_call = get_keycloak_admin(mock_settings)
    second_call = get_keycloak_admin(mock_settings)

    assert first_call is second_call
    mock_admin_class.assert_called_once()


@patch.object(dependencies, KeycloakAdmin.__name__)
@patch.object(dependencies, KeycloakOpenIDConnection.__name__)
def test_get_keycloak_admin_uses_settings(mock_conn: MagicMock, _: MagicMock) -> None:
    mock_settings = MagicMock()
    mock_settings.keycloak_server_url = "http://localhost:9000/auth/"
    mock_settings.keycloak_realm = "slas"
    mock_settings.client_id = "test_client"
    mock_settings.client_secret = "test_secret"

    get_keycloak_admin(mock_settings)

    call_kwargs = mock_conn.call_args.kwargs
    assert "server_url" in call_kwargs
    assert "realm_name" in call_kwargs
    assert "client_id" in call_kwargs
    assert "client_secret_key" in call_kwargs
    assert call_kwargs["verify"] is True
