from unittest.mock import Mock

import pytest
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database.orm import import_tables
from app.database.tables.base import DbBase


@pytest.fixture(scope="session")
def db_session() -> Session:
    with PostgresContainer("postgres:16.1") as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url(), pool_pre_ping=True)
        import_tables()
        DbBase.metadata.create_all(bind=engine, checkfirst=True)

        session = sessionmaker(bind=engine)()
        try:
            yield session
        finally:
            session.close()
            engine.dispose()


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

