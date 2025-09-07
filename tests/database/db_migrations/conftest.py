from pathlib import Path

import pytest
from alembic.config import Config
from sqlalchemy import Engine, MetaData
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture(scope="session")
def migration_config(db_engine: Engine) -> Config:
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
def migration_meta_data(migration_config: Config, db_engine: Engine) -> MetaData:
    meta_data = MetaData()
    meta_data.reflect(bind=db_engine)
    yield meta_data


@pytest.fixture(scope="function")
def migration_session(db_engine: Engine, migration_meta_data: MetaData) -> Session:
    session = sessionmaker(bind=db_engine)()
    try:
        yield session
    finally:
        migration_meta_data.drop_all(bind=db_engine, checkfirst=True)
        session.close()
