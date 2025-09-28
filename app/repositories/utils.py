import logging
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Iterable, Type, TypeAlias, TypeVar
from uuid import UUID

from sqlalchemy import ColumnCollection, and_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute, Session
from sqlalchemy.sql.schema import ColumnCollectionConstraint, Index

from app.database.exceptions import EntryNotFoundError

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=DeclarativeBase)
OnUpdateConstraint: TypeAlias = str | ColumnCollectionConstraint | Index | None
OnUpdateFields: TypeAlias = Mapping[Any, Any] | ColumnCollection | None


def add_entry(session: Session, db: T) -> None:
    session.add(db)
    session.flush()


def get_by_id(session: Session, _class: Type[T], _id: UUID) -> T | None:
    return session.execute(select(_class).filter_by(id=_id)).unique().scalar_one_or_none()


async def aget_by_id(session: AsyncSession, _class: Type[T], _id: UUID) -> T | None:
    result = await session.execute(select(_class).filter_by(id=_id))
    return result.unique().scalar_one_or_none()


def get_all(session: Session, _class: Type[T], filter_by: dict[InstrumentedAttribute, Any] = None) -> Iterable[T]:
    query = select(_class)
    if filter_by:
        logger.debug(
            "Filter used in querying %(_class)s: %(filter)r",
            {"_class": _class.__name__, "filter": filter_by}
        )
        conditions = [key == value for key, value in filter_by.items()]
        query = query.where(and_(*conditions))
    return session.execute(query).unique().scalars().all()


async def aget_all(session: AsyncSession, _class: Type[T], filter_by: dict[InstrumentedAttribute, Any] = None) -> Iterable[T]:
    query = select(_class)
    if filter_by:
        logger.debug(
            "Filter used in querying %(_class)s: %(filter)r",
            {"_class": _class.__name__, "filter": filter_by}
        )
        conditions = [key == value for key, value in filter_by.items()]
        query = query.where(and_(*conditions))
    result = await session.execute(query)
    return result.unique().scalars().all()


def update_entry(session: Session, _class: Type[T], _id: UUID, **kwargs) -> None:
    session.execute(update(_class).where(_class.id == _id).values(**kwargs))
    session.flush()


def upsert_entry(
        session: Session,
        db: T,
        on_constraint: OnUpdateConstraint,
        fields_to_update: OnUpdateFields
) -> None:
    db_class: Type[T] = db.__class__
    insert_stmt = insert(db_class).values(
        **{
            k: v for k, v in db.__dict__.items()
            if not k.startswith("_")
        }
    )
    upsert_stmt = insert_stmt.on_conflict_do_update(
        constraint=on_constraint,
        set_={
            **fields_to_update,
            db_class.modified_at: datetime.now(timezone.utc)
        }
    )
    session.execute(upsert_stmt)


def delete_entry(session: Session, _class: Type[T], _id: UUID) -> None:
    entry = session.get(_class, _id)
    if entry is None:
        raise EntryNotFoundError(
            f"Table '{_class.__tablename__}' has no entry with id '{_id}'."
        )
    session.delete(entry)
    session.flush()
