from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.orm import Session


def test_upgrade(migration_config: Config, migration_session: Session) -> None:
    has_no_tables_in_public_schema(db_session=migration_session)
    has_not_enum_mediatype(db_session=migration_session)

    command.upgrade(migration_config, "95430add6996")

    has_right_alembic_version(db_session=migration_session)
    has_defined_tables(db_session=migration_session)
    has_enum_mediatype(db_session=migration_session)


def test_downgrade(migration_config: Config, migration_session: Session)-> None:
    has_right_alembic_version(db_session=migration_session)
    has_defined_tables(db_session=migration_session)
    has_enum_mediatype(db_session=migration_session)

    command.downgrade(migration_config, "base")

    has_no_tables_in_public_schema(db_session=migration_session)
    has_not_enum_mediatype(db_session=migration_session)


def test_multiple_walkings_from_base_works(migration_config: Config) -> None:
    for _ in range(3):
        command.upgrade(migration_config, "95430add6996")
        command.downgrade(migration_config, "base")


def has_no_tables_in_public_schema(db_session: Session) -> None:
    stmt = "SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name != 'alembic_version'"
    tables = db_session.execute(text(stmt)).fetchall()
    assert len(tables) == 0


def has_right_alembic_version(db_session: Session) -> None:
    stmt = "SELECT * FROM alembic_version WHERE version_num = '95430add6996'"
    result = db_session.execute(text(stmt))
    assert result.scalar_one() == "95430add6996"


def has_defined_tables(db_session: Session) -> None:
    expected_tables = {
        "alembic_version", "assessments", "assessments_tasks",
        "bucket_objects", "choices", "multiple_choices_choices", "exercises",
        "multiple_choices", "primers", "submissions", "tasks",
    }
    stmt = "SELECT * FROM information_schema.tables"
    tables = db_session.execute(text(stmt)).fetchall()
    assert all(et in {t.table_name for t in tables} for et in expected_tables)


def has_enum_mediatype(db_session: Session) -> None:
    stmt = "SELECT * FROM pg_type WHERE typname = 'mediatype'"
    result = db_session.execute(text(stmt)).fetchall()
    assert len(result) == 1


def has_not_enum_mediatype(db_session: Session) -> None:
    stmt = "SELECT * FROM pg_type WHERE typname = 'mediatype'"
    result = db_session.execute(text(stmt)).fetchall()
    assert len(result) == 0
