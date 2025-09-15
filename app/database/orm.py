import logging
from typing import Annotated, Iterator
from urllib.parse import quote

from alembic import command
from alembic.config import Config
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings
from app.database.tables.base import DbBase
from app.settings import get_settings

logger = logging.getLogger(__name__)

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
    logger.debug("Creating new database session.")
    with session_factory.begin() as session:  # pylint: disable=no-member
        logger.debug("Session created.")
        yield session
        try:
            logger.debug("Committing database session objects.")
            session.commit()
        except SQLAlchemyError as exc:
            logger.exception(exc)
            logger.error("Rolling back database session objects.")
            session.rollback()


def import_tables() -> None:
    """Tables have to be imported in declarative mapping style"""
    # pylint: disable=wrong-import-position,import-outside-toplevel
    from app.database.tables.assessment_submissions import DbAssessmentSubmission
    from app.database.tables.assessments import DbAssessment
    from app.database.tables.assessments_tasks import DbAssessmentsTasks
    from app.database.tables.bucket_objects import DbBucketObjects
    from app.database.tables.choices import DbChoice
    from app.database.tables.exercise_submissions import DbExerciseSubmission
    from app.database.tables.exercises import DbExercise
    from app.database.tables.multiple_choices import DbMultipleChoice
    from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
    from app.database.tables.primers import DbPrimer
    from app.database.tables.tasks import DbTask

    _ = (  # use imports to prevent them automatically stripped away by IDE
        DbAssessment, DbAssessmentSubmission, DbAssessmentsTasks,
        DbBucketObjects, DbChoice, DbExercise, DbExerciseSubmission,
        DbMultipleChoice, DbMultipleChoicesChoices, DbPrimer, DbTask
    )


def run_migrations():  # pragma: no cover
    logger.info("Configures alembic and runs migrations.")
    alembic_cfg = Config("alembic.ini")
    logger.info("Running migrations to latest revision.")
    try:
        command.upgrade(alembic_cfg, "head")
        logger.info("Running migrations to latest revision finished.")
    except Exception as exc:
        logger.exception(exc)
        logger.error("Running migrations to latest revision failed.")
        raise


def init_db(engine: Annotated[Engine, Depends(get_db_engine)]) -> None:
    import_tables()
    logger.info("Creating database tables.")
    DbBase.metadata.create_all(bind=engine, checkfirst=True)
    logger.info("Database tables created.")
