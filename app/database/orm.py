from functools import lru_cache
from typing import Annotated, Iterator
from urllib.parse import quote

from fastapi import Depends
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import Session, registry, sessionmaker

from app.config import Settings
from app.core.models.submission import Submission
from app.database.metadata import metadata_obj
from app.database.tables.submissions import submissions
from app.rest.settings import get_settings


@lru_cache
def get_db_session_factory(db_host: str, db_user: str, db_password: str) -> sessionmaker:
    engine = sqlalchemy_create_engine(
        f"postgresql+psycopg2://{db_user}:{quote(db_password)}@{db_host}/backend"
    )
    metadata_obj.create_all(bind=engine, checkfirst=True)
    mapper_registry = registry()
    mapper_registry.map_imperatively(Submission, submissions)
    return sessionmaker(bind=engine)


def get_db_session(settings: Annotated[Settings, Depends(get_settings)]) -> Iterator[Session]:
    session_factory = get_db_session_factory(
        db_host=settings.db_host,
        db_user=settings.db_user,
        db_password=settings.db_password
    )
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
