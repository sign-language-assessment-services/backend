from _pytest.monkeypatch import MonkeyPatch

from app.config import Settings


def test_default_is_taken(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("DB_USER", "db_testuser")
    monkeypatch.setenv("DB_PASSWORD", "db_testpassword")
    monkeypatch.setenv("DB_HOST", "db_testhost")
    monkeypatch.setenv("CLIENT_ID", "clientid")
    monkeypatch.setenv("CLIENT_SECRET", "clientsecret")
    assert Settings().data_bucket_name == "slportal"


def test_env_variable_is_taken(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("DB_USER", "db_testuser")
    monkeypatch.setenv("DB_PASSWORD", "db_testpassword")
    monkeypatch.setenv("DB_HOST", "db_testhost")
    monkeypatch.setenv("DATA_BUCKET_NAME", "foobar")
    monkeypatch.setenv("CLIENT_ID", "clientid")
    monkeypatch.setenv("CLIENT_SECRET", "clientsecret")
    assert Settings().data_bucket_name == "foobar"
