from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.orm import Session

VERSION = "6c37a4dce403"
CHILD_VERSION = "c7ae71fc77b5"


def test_upgrade(migration_config: Config, migration_session: Session) -> None:
    command.upgrade(migration_config, CHILD_VERSION)
    has_not_unique_identifier_in_submission_exercise(db_session=migration_session)

    command.upgrade(migration_config, VERSION)

    has_unique_identifier_in_submission_exercise(db_session=migration_session)


def test_downgrade(migration_config: Config, migration_session: Session)-> None:
    command.upgrade(migration_config, VERSION)
    has_unique_identifier_in_submission_exercise(db_session=migration_session)

    command.downgrade(migration_config, CHILD_VERSION)

    has_not_unique_identifier_in_submission_exercise(db_session=migration_session)


def test_multiple_walkings_from_base_works(migration_config: Config) -> None:
    for _ in range(3):
        command.upgrade(migration_config, VERSION)
        command.downgrade(migration_config, "base")


def has_unique_identifier_in_submission_exercise(db_session: Session) -> None:
    stmt = """
        SELECT conname
        FROM pg_constraint
        WHERE conrelid = (
            SELECT oid 
            FROM pg_class
            WHERE relname LIKE 'exercise_submissions'
        );
    """
    constraints = [constraint[0] for constraint in db_session.execute(text(stmt)).fetchall()]
    assert "exercise_submissions_assessment_submission_id_exercise_id_key" in constraints


def has_not_unique_identifier_in_submission_exercise(db_session: Session) -> None:
    stmt = """
        SELECT conname
        FROM pg_constraint
        WHERE conrelid = (
            SELECT oid 
            FROM pg_class
            WHERE relname LIKE 'exercise_submissions'
        );
    """
    constraints = [constraint[0] for constraint in db_session.execute(text(stmt)).fetchall()]
    assert "exercise_submissions_assessment_submission_id_exercise_id_key" not in constraints
