from _pytest.monkeypatch import MonkeyPatch

from app.config import Settings


def test_default_is_taken() -> None:
    assert Settings().data_bucket_name == "slportal"


def test_env_variable_is_taken(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("DATA_BUCKET_NAME", "foobar")
    assert Settings().data_bucket_name == "foobar"
