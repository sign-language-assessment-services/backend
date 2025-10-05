import contextlib
from unittest.mock import MagicMock, patch

from sqlalchemy import Engine, inspect
from sqlalchemy.exc import SQLAlchemyError

import app.database.orm as orm_module
from app.database.orm import get_db_engine, get_db_session, get_sessionmaker, import_tables, init_db
from app.database.tables.base import DbBase
from tests.database.utils import get_all_table_names_from_tables_folder
from tests.settings_for_tests import TestSettings


@patch.object(orm_module, orm_module.get_settings.__name__, return_value=TestSettings())
def test_get_db_engine_reflects_settings(_: MagicMock, settings: TestSettings) -> None:
    engine = get_db_engine()

    assert engine.name == settings.db_type
    assert engine.driver == settings.db_driver
    assert engine.url.database == settings.db_name
    assert engine.url.host == settings.db_host
    assert engine.url.password == settings.db_password
    assert engine.url.port == settings.db_port
    assert engine.url.username == settings.db_user
    assert engine.pool._max_overflow == settings.db_max_overflow
    assert engine.pool._pool.maxsize == settings.db_pool_size
    assert engine.pool._pre_ping == settings.db_pool_pre_ping
    assert engine.pool._recycle == settings.db_pool_recycle
    assert engine.echo == settings.db_echo


@patch.object(orm_module, orm_module.get_settings.__name__, return_value=TestSettings())
def test_get_db_session_binds_engine(_: MagicMock) -> None:
    engine = get_db_engine()

    session = next(get_db_session(session_factory=get_sessionmaker()))

    assert session.bind is engine


@patch.object(orm_module, orm_module.get_settings.__name__, return_value=TestSettings())
def test_get_db_session_performs_rollback_on_sqlalchemy_error(_: MagicMock, db_engine: Engine) -> None:
    with patch("app.database.orm.logger") as mock_logger:
        session_generator = get_db_session(session_factory=get_sessionmaker())
        session = next(session_generator)

        with patch.object(session, "rollback") as mock_rollback:
            with contextlib.suppress(SQLAlchemyError):
                session_generator.throw(SQLAlchemyError("Test database error"))

    mock_rollback.assert_called_once()
    mock_logger.exception.assert_called_once()


@patch.object(orm_module, orm_module.get_settings.__name__, return_value=TestSettings())
def test_all_tables_are_imported(_: MagicMock) -> None:
    import_tables()

    db_tables = set(DbBase.metadata.tables)
    tables = get_all_table_names_from_tables_folder()
    assert db_tables == tables


@patch.object(orm_module, orm_module.get_settings.__name__, return_value=TestSettings())
def test_init_db_creates_tables(_: MagicMock, db_engine_reset: Engine) -> None:
    init_db(engine=db_engine_reset)

    table_names = inspect(db_engine_reset).get_table_names()
    assert set(DbBase.metadata.tables) == set(table_names)
