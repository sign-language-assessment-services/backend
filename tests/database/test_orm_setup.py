import contextlib
from unittest.mock import patch

from sqlalchemy import Engine, inspect
from sqlalchemy.exc import SQLAlchemyError

from app.config import Settings
from app.database.orm import get_db_engine, get_db_session, import_tables, init_db
from app.database.tables.base import DbBase
from tests.database.utils import get_all_table_names_from_tables_folder


def test_get_db_engine_reflects_settings(settings: Settings) -> None:
    engine = get_db_engine(settings=settings)

    assert engine.name == "postgresql"
    assert engine.driver == "psycopg2"
    assert engine.url.database == settings.db_user
    assert engine.url.host == settings.db_host
    assert engine.url.password == settings.db_password
    assert engine.url.username == settings.db_user


def test_get_db_session_binds_engine(settings: Settings) -> None:
    engine = get_db_engine(settings=settings)

    session = next(get_db_session(engine=engine))

    assert session.bind is engine


def test_get_db_session_performs_rollback_on_sqlalchemy_error(db_engine: Engine) -> None:
    with patch("app.database.orm.logger") as mock_logger:
        session_generator = get_db_session(engine=db_engine)
        session = next(session_generator)

        with patch.object(session, "rollback") as mock_rollback:
            with contextlib.suppress(StopIteration, SQLAlchemyError):
                session_generator.throw(SQLAlchemyError("Test database error"))

    mock_rollback.assert_called_once()
    mock_logger.exception.assert_called_once()
    mock_logger.error.assert_called_once_with("Rolling back database session objects.")


def test_all_tables_are_imported() -> None:
    import_tables()

    db_tables = set(DbBase.metadata.tables)
    tables = get_all_table_names_from_tables_folder()
    assert db_tables == tables


def test_init_db_creates_tables(db_engine_reset: Engine) -> None:
    init_db(engine=db_engine_reset)

    table_names = inspect(db_engine_reset).get_table_names()
    assert set(DbBase.metadata.tables) == set(table_names)
