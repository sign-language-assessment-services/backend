from typing import Generator

import pytest
from pydantic_settings import BaseSettings
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database.orm import import_tables
from app.database.tables.base import DbBase


def _db_engine_fixture(test_settings: BaseSettings) -> Generator[Engine, None, None]:
    with PostgresContainer(
        image="postgres:17.6",
        username=test_settings.db_user,
        password=test_settings.db_password,
        dbname=test_settings.db_name,
        driver=test_settings.db_driver
    ) as postgres:
        engine = create_engine(
            url=postgres.get_connection_url(),
            max_overflow=test_settings.db_max_overflow,
            pool_pre_ping=test_settings.db_pool_pre_ping,
            pool_size=test_settings.db_pool_size,
            pool_timeout=test_settings.db_pool_timeout,
            pool_recycle=test_settings.db_pool_recycle,
            echo=test_settings.db_echo,
            echo_pool=test_settings.db_echo_pool
        )
        try:
            yield engine
        finally:
            engine.dispose()


@pytest.fixture(scope="session")
def db_engine(settings: BaseSettings) -> Generator[Engine, None, None]:
    yield from _db_engine_fixture(settings)


@pytest.fixture(scope="function")
def db_engine_reset(settings: BaseSettings) -> Generator[Engine, None, None]:
    yield from _db_engine_fixture(settings)


@pytest.fixture(scope="function")
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    import_tables()
    DbBase.metadata.create_all(bind=db_engine)

    session = sessionmaker(bind=db_engine)()
    try:
        yield session
    finally:
        session.close()
        DbBase.metadata.drop_all(db_engine, checkfirst=True)
