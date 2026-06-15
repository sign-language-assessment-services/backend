import httpx

from tests.settings_for_tests import TestSettings


def _keycloak_is_reachable() -> bool:
    try:
        response = httpx.get(SETTINGS.keycloak_server_url, timeout=2)
        return response.status_code < 500
    except httpx.TransportError:
        return False


THEO_USERNAME = "theo@a.de"
SETTINGS = TestSettings()
