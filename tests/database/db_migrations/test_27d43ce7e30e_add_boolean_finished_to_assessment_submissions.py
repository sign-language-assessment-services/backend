from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.orm import Session

VERSION = "27d43ce7e30e"
CHILD_VERSION = "2147c19c1d38"


def test_upgrade(migration_config: Config, migration_session: Session) -> None:
    command.upgrade(migration_config, CHILD_VERSION)
    has_no_finished_column_in_assessment_submissions(db_session=migration_session)

    command.upgrade(migration_config, VERSION)

    has_finished_column_in_assessment_submissions(db_session=migration_session)


def test_downgrade(migration_config: Config, migration_session: Session)-> None:
    command.upgrade(migration_config, VERSION)
    has_finished_column_in_assessment_submissions(db_session=migration_session)

    command.downgrade(migration_config, CHILD_VERSION)

    has_no_finished_column_in_assessment_submissions(db_session=migration_session)


def test_multiple_walkings_from_base_works(migration_config: Config) -> None:
    for _ in range(3):
        command.upgrade(migration_config, VERSION)
        command.downgrade(migration_config, "base")


def has_finished_column_in_assessment_submissions(db_session: Session) -> None:
    stmt = """
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'assessment_submissions' AND column_name = 'finished';
    """
    columns = db_session.execute(text(stmt)).fetchall()
    assert len(columns) == 1


def has_no_finished_column_in_assessment_submissions(db_session: Session) -> None:
    stmt = """
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'assessment_submissions' AND column_name = 'finished';
    """
    columns = db_session.execute(text(stmt)).fetchall()
    assert len(columns) == 0
