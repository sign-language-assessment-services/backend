import pytest
from sqlalchemy import create_engine, Engine
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
