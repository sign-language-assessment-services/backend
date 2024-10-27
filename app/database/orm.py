from __future__ import annotations

from typing import Annotated, Iterator
from urllib.parse import quote

from alembic import command
from alembic.config import Config
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings
from app.database.tables.base import DbBase
from app.settings import get_settings


def get_db_engine(settings: Annotated[Settings, Depends(get_settings)]) -> Engine:
    connection_url = "{db_type}+{driver}://{user}:{password}@{host}/{db_name}"
    return create_engine(
        connection_url.format(
            db_type="postgresql",
            driver="psycopg2",
            user=quote(settings.db_user),
            password=quote(settings.db_password),
            host=quote(settings.db_host),
            db_name=quote(settings.db_user)
        )
    )


def get_db_session(engine: Annotated[Engine, Depends(get_db_engine)]) -> Iterator[Session]:
    session_factory = sessionmaker(bind=engine)
    with session_factory.begin() as session:  # pylint: disable=no-member
        yield session


def import_tables() -> None:
    """Tables have to be imported in declarative mapping style"""
    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.database.tables.assessments import DbAssessment
    from app.database.tables.assessments_tasks import assessment_tasks
    from app.database.tables.buckets import DbBucket
    from app.database.tables.choices import DbChoice
    from app.database.tables.exercises import DbExercise
    from app.database.tables.multiple_choice_submissions import DbMultipleChoiceSubmission
    from app.database.tables.multiple_choices import DbMultipleChoice
    from app.database.tables.primers import DbPrimer
    from app.database.tables.submissions import DbSubmission
    from app.database.tables.submissions_choices import submissions_choices
    from app.database.tables.tasks import DbTask
    from app.database.tables.text_submissions import DbTextSubmission
    from app.database.tables.texts import DbText
    # use imports to prevent them stripped away by IDE
    _ = (
        DbAssessment, assessment_tasks, DbBucket, DbChoice, DbExercise,
        DbMultipleChoiceSubmission, DbMultipleChoice, DbPrimer, DbSubmission,
        submissions_choices, DbTask, DbTextSubmission, DbText
    )

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def init_db(engine: Annotated[Engine, Depends(get_db_engine)]) -> None:
    import_tables()
    DbBase.metadata.create_all(bind=engine, checkfirst=True)
