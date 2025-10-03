import logging
import time
from functools import cache
from typing import Annotated, Generator

from alembic import command
from alembic.config import Config
from fastapi import Depends
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.tables.base import DbBase
from app.settings import get_settings

logger = logging.getLogger(__name__)


@cache
def get_db_engine() -> Engine:
    settings = get_settings()
    connection_url = URL.create(
        drivername=f"{settings.db_type}+{settings.db_driver}",
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )
    return create_engine(
        connection_url,
        max_overflow=settings.db_max_overflow,
        pool_pre_ping=settings.db_pool_pre_ping,
        pool_size=settings.db_pool_size,
        pool_timeout=settings.db_pool_timeout,
        pool_recycle=settings.db_pool_recycle,
        echo=settings.db_echo,
        echo_pool=settings.db_echo_pool
    )


@cache
def get_sessionmaker() -> sessionmaker:
    settings = get_settings()
    return sessionmaker(
        class_=Session,
        expire_on_commit=settings.db_expire_on_commit,
        autoflush=settings.db_autoflush
    )


def get_db_session(
        session_factory: Annotated[sessionmaker, Depends(get_sessionmaker)]
) -> Generator[Session, None, None]:
    session = session_factory(bind=get_db_engine())
    logger.info(
        "New database session %(session_id)s created for engine %(engine_id)s.",
        {"session_id": id(session), "engine_id": id(session.get_bind())},
    )
    try:
        yield session
    except Exception:
        logger.exception("Error in session %(_id)s. Rolling back.", {"_id": id(session)})
        session.rollback()
        raise
    finally:
        logger.info("Closing database session %(_id)s.", {"_id": id(session)})
        session.close()


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
    logger.info("Configure alembic.")
    alembic_cfg = Config("alembic.ini")
    logger.info("Running migrations to latest revision.")
    try:
        start_time = time.time()
        command.upgrade(alembic_cfg, "head")
        end_time = time.time()
        logger.info(
            "Running migrations to latest revision finished in %(duration).2f seconds.",
            {"duration": end_time - start_time}
        )
    except Exception as exc:
        logger.exception(exc)
        logger.error("Running migrations to latest revision failed.")
        raise


def init_db(engine: Annotated[Engine, Depends(get_db_engine)]) -> None:
    import_tables()
    logger.info("Creating database tables.")
    DbBase.metadata.create_all(bind=engine, checkfirst=True)
    logger.info("Database tables created.")
