import os
from pathlib import Path
from unittest.mock import Mock

import pytest
from alembic.config import Config
from sqlalchemy import Engine, MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database.orm import import_tables
from app.database.tables.base import DbBase


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    with PostgresContainer("postgres:16.1") as postgres:
        engine = create_engine(postgres.get_connection_url(), pool_pre_ping=True)
        try:
            yield engine
        finally:
            engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine: Engine) -> Session:
    import_tables()
    DbBase.metadata.create_all(bind=db_engine)

    session = sessionmaker(bind=db_engine)()
    try:
        yield session
    finally:
        session.close()
        DbBase.metadata.drop_all(db_engine, checkfirst=True)


@pytest.fixture
def settings() -> Mock:
    settings = Mock()
    settings.data_endpoint = "127.0.0.1:4242"
    settings.data_bucket_name = "testbucket"
    settings.data_root_user = "testuser"
    settings.data_root_password = "testpassword"
    settings.data_secure = False
    settings.db_user = "testuser"
    settings.db_password = "testpassword"
    settings.db_host = "localhost"
    return settings


@pytest.fixture(scope="session")
def migration_config(db_engine: Engine) -> Config:
    project_root = Path(__file__).parent.parent.resolve()
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
