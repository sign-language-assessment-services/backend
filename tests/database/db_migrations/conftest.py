from pathlib import Path
from typing import Generator

import pytest
from _pytest.monkeypatch import MonkeyPatch
from alembic.config import Config
from sqlalchemy import Engine, MetaData
from sqlalchemy.orm import Session, sessionmaker

from tests.settings_for_tests import TestSettings


@pytest.fixture(autouse=True)
def prevent_loading_dotenv_in_migration_tests(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("dotenv.load_dotenv", lambda *args, **kwargs: False, raising=False)


@pytest.fixture(autouse=True)
def env_variables_needed_for_migration_config(monkeypatch: MonkeyPatch) -> None:
    test_settings = TestSettings()
    monkeypatch.setenv("DB_USER", test_settings.db_user)
    monkeypatch.setenv("DB_PASSWORD", test_settings.db_password)
    monkeypatch.setenv("DB_NAME", test_settings.db_name)
    monkeypatch.setenv("DB_HOST", test_settings.db_host)
    monkeypatch.setenv("DB_PORT", str(test_settings.db_port))


@pytest.fixture(scope="session")
def migration_config(db_engine: Engine) -> Generator[Config, None, None]:
    project_root = Path(__file__).parent.parent.parent.parent.resolve()
    sqlalchemy_url = (
        f"postgresql://{db_engine.url.username}:{db_engine.url.password}@"
        f"{db_engine.url.host}:{db_engine.url.port}/{db_engine.url.database}"
    )
    alembic_config = Config()
    alembic_config.set_main_option("script_location", str(project_root / "db_migrations"))
    alembic_config.set_main_option("sqlalchemy.url", sqlalchemy_url)
    yield alembic_config


@pytest.fixture(scope="session")
def migration_meta_data(migration_config: Config, db_engine: Engine) -> Generator[MetaData, None, None]:
    meta_data = MetaData()
    meta_data.reflect(bind=db_engine)
    yield meta_data


@pytest.fixture(scope="function")
def migration_session(db_engine: Engine, migration_meta_data: MetaData) -> Generator[Session, None, None]:
    session = sessionmaker(bind=db_engine)()
    try:
        yield session
    finally:
        migration_meta_data.drop_all(bind=db_engine, checkfirst=True)
        session.close()
