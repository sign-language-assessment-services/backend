from typing import Type

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.tables.base import DbBase


def table_count(db_session: Session, table: Type[DbBase]) -> int:
    return db_session.scalar(select(func.count()).select_from(table))
