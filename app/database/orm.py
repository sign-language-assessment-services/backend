from __future__ import annotations

from typing import Annotated, Iterator
from urllib.parse import quote

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings
from app.database.tables.base import Base
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


def init_db(engine: Annotated[Engine, Depends(get_db_engine)]) -> None:
    # The table classes have to be imported before using create_all method.
    # pylint: disable=wrong-import-position,import-outside-toplevel,unused-import
    from app.database.tables.assessments import DbAssessment
    from app.database.tables.choices import DbChoice
    from app.database.tables.exercises import DbExercise
    from app.database.tables.multimedia_files import DbMultiMediaFiles
    from app.database.tables.primers import DbPrimer
    from app.database.tables.submissions import DbSubmission
    Base.metadata.create_all(bind=engine, checkfirst=True)


def get_db_session(engine: Annotated[Engine, Depends(get_db_engine)]) -> Iterator[Session]:
    session_factory = sessionmaker(bind=engine)
    with session_factory.begin() as session:  # pylint: disable=no-member
        yield session
