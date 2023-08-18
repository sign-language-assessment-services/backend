from unittest.mock import Mock, patch

from app.config import Settings
from app.rest.settings import get_settings


def test_get_settings() -> None:
    assert get_settings() == Settings()


@patch("app.rest.settings.Settings")
def test_get_settings_calls_settings_class_only_once(settings_class: Mock) -> None:
    get_settings.cache_clear()

    get_settings()
    get_settings()

    settings_class.assert_called_once()
