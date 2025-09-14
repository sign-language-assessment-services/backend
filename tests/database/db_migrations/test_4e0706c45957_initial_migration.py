from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.orm import Session

VERSION = "4e0706c45957"
CHILD_VERSION = "base"


def test_upgrade(migration_config: Config, migration_session: Session) -> None:
    command.upgrade(migration_config, CHILD_VERSION)
    has_no_tables_in_public_schema(db_session=migration_session)
    has_not_enum_mediatype(db_session=migration_session)

    command.upgrade(migration_config, VERSION)

    has_right_alembic_version(db_session=migration_session)
    has_defined_tables(db_session=migration_session)
    has_enum_mediatype(db_session=migration_session)


def test_downgrade(migration_config: Config, migration_session: Session)-> None:
    command.upgrade(migration_config, VERSION)
    has_right_alembic_version(db_session=migration_session)
    has_defined_tables(db_session=migration_session)
    has_enum_mediatype(db_session=migration_session)

    command.downgrade(migration_config, CHILD_VERSION)

    has_no_tables_in_public_schema(db_session=migration_session)
    has_not_enum_mediatype(db_session=migration_session)


def test_multiple_walkings_from_base_works(migration_config: Config) -> None:
    for _ in range(3):
        command.upgrade(migration_config, VERSION)
        command.downgrade(migration_config, "base")


def has_no_tables_in_public_schema(db_session: Session) -> None:
    stmt = """
        SELECT * FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name != 'alembic_version'
    """
    tables = db_session.execute(text(stmt)).fetchall()
    assert len(tables) == 0


def has_right_alembic_version(db_session: Session) -> None:
    stmt = f"SELECT * FROM alembic_version WHERE version_num = '{VERSION}'"
    result = db_session.execute(text(stmt))
    assert result.scalar_one() == VERSION


def has_defined_tables(db_session: Session) -> None:
    expected_tables = {
        "alembic_version", "assessment_submissions", "assessments",
        "assessments_tasks", "bucket_objects", "choices",
        "exercise_submissions", "exercises", "multiple_choices",
        "multiple_choices_choices", "primers", "tasks"
    }
    stmt = "SELECT * FROM information_schema.tables WHERE table_schema = 'public'"
    tables = db_session.execute(text(stmt)).fetchall()
    assert {t.table_name for t in tables} == expected_tables


def has_enum_mediatype(db_session: Session) -> None:
    stmt = "SELECT * FROM pg_type WHERE typname = 'mediatype'"
    result = db_session.execute(text(stmt)).fetchall()
    assert len(result) == 1


def has_not_enum_mediatype(db_session: Session) -> None:
    stmt = "SELECT * FROM pg_type WHERE typname = 'mediatype'"
    result = db_session.execute(text(stmt)).fetchall()
    assert len(result) == 0
