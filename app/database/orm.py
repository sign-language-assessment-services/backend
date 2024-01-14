from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Iterator
from urllib.parse import quote

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings
from app.database.tables.base import Base
from app.rest.settings import get_settings


@lru_cache
def get_db_session_factory(db_host: str, db_user: str, db_password: str) -> sessionmaker[Session]:
    engine = create_engine(f"postgresql+psycopg2://{db_user}:{quote(db_password)}@{db_host}/backend")
    Base.metadata.create_all(bind=engine, checkfirst=True)

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
