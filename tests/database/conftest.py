import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database.orm import init_db
from app.database.tables.base import DbBase


@pytest.fixture(scope="session")
def db_engine():
    with PostgresContainer("postgres:16") as postgres:
        test_engine = create_engine(
            postgres.get_connection_url(),
            pool_pre_ping=True
        )
        yield test_engine
        test_engine.dispose()


@pytest.fixture(scope="function", autouse=True)
def db_tables(db_engine):
    init_db(engine=db_engine)
    yield
    DbBase.metadata.drop_all(db_engine)


@pytest.fixture(scope="function")
def db_session(db_engine, db_tables):
    session_factory = sessionmaker(bind=db_engine)
    with session_factory.begin() as session:  # pylint: disable=no-member
        yield session
