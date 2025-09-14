from unittest.mock import MagicMock, patch

from sqlalchemy import Engine, inspect
from sqlalchemy.exc import SQLAlchemyError

import app.database.orm as orm_module
from app.config import Settings
from app.database.orm import get_db_engine, get_db_session, import_tables, init_db, sessionmaker
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


@patch.object(orm_module, sessionmaker.__name__)
def test_get_db_session_rollbacks_on_error(mock_sessionmaker: MagicMock, settings: Settings) -> None:
    mock_session = MagicMock()
    mock_sessionmaker.return_value.begin.return_value.__enter__.return_value = mock_session
    mock_session.commit.side_effect = SQLAlchemyError("Error test message")

    for _ in get_db_session(engine=get_db_engine(settings=settings)):
        pass

    mock_session.commit.assert_called_once()
    mock_session.rollback.assert_called_once()


def test_all_tables_are_imported() -> None:
    import_tables()

    db_tables = set(DbBase.metadata.tables)
    tables = get_all_table_names_from_tables_folder()
    assert db_tables == tables


def test_init_db_creates_tables(db_engine_reset: Engine) -> None:
    init_db(engine=db_engine_reset)

    table_names = inspect(db_engine_reset).get_table_names()
    assert set(DbBase.metadata.tables) == set(table_names)
