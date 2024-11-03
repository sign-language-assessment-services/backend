from unittest.mock import Mock

import pytest
import sqlalchemy
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database.orm import import_tables
from app.database.tables.base import DbBase


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    with PostgresContainer("postgres:16.1") as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url(), pool_pre_ping=True)
        yield engine
        engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Session:
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

