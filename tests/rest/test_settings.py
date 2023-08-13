from app.config import Settings
from app.rest.settings import get_settings


def test_get_settings() -> None:
    assert get_settings() == Settings()
