from unittest.mock import Mock, patch

from _pytest.monkeypatch import MonkeyPatch

from app.config import Settings
from app.rest.settings import get_settings


def test_get_settings(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("DB_USER", "db_testuser")
    monkeypatch.setenv("DB_PASSWORD", "db_testpassword")
    monkeypatch.setenv("DB_HOST", "db_testhost")
    assert get_settings() == Settings()


@patch("app.rest.settings.Settings")
def test_get_settings_calls_settings_class_only_once(settings_class: Mock) -> None:
    get_settings.cache_clear()

    get_settings()
    get_settings()

    settings_class.assert_called_once()
