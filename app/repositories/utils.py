import logging
from collections.abc import Mapping
from typing import Any, Iterator, Type, TypeAlias, TypeVar
from uuid import UUID

from sqlalchemy import func, inspect, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import InstrumentedAttribute, Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.sql.schema import ColumnCollectionConstraint, Index

from app.database.exceptions import EntryNotFoundError
from app.database.tables.base import DbBase

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=DbBase)
OnUpdateConstraint: TypeAlias = str | ColumnCollectionConstraint | Index | None


def add_entry(session: Session, db: T, commit: bool = True) -> None:
    logger.info(
        "Using generic database request to add %(_id)s from %(_class)s with session id %(session_id)s.",
        {"_id": db.id, "_class": db.__class__.__name__, "session_id": id(session)}
    )
    session.add(db)
    if commit:
        session.commit()


def get_by_id(session: Session, _class: Type[T], _id: UUID) -> T | None:
    logger.info(
        "Using generic database request to receive %(_id)s from %(_class)s with session id %(session_id)s.",
        {"_id": _id, "_class": _class.__name__, "session_id": id(session)}
    )
    return session.get(_class, _id)


def get_all(session: Session, _class: Type[T], filters: dict[InstrumentedAttribute, Any] = None) -> Iterator[T]:
    query = select(_class)
    if filters:
        logger.info(
            "Querying %(_class)s with filters: %(filters)r",
            {"_class": _class.__name__, "filters": filters}
        )
        for column, value in filters.items():
            query = query.where(column == value)
    logger.info(
        "Using generic database request to receive all from %(_class)s with session id %(session_id)s.",
        {"_class": _class.__name__, "session_id": id(session)}
    )
    return session.execute(query).scalars()


def update_entry(session: Session, _class: Type[T], _id: UUID, commit: bool = True, **kwargs) -> None:
    logger.info(
        "Using generic database request to update %(_id)s from %(_class)s with session id %(session_id)s.",
        {"_id": _id, "_class": _class.__name__, "session_id": id(session)}
    )
    session.execute(update(_class).where(_class.id == _id).values(**kwargs))
    if commit:
        session.commit()


def upsert_entry(
        session: Session,
        db: T,
        on_constraint: OnUpdateConstraint,
        fields_to_update: Mapping[Any, Any],
        commit: bool = True
) -> None:
    db_class: Type[T] = type(db)
    logger.info(
        "Using generic database request to upsert %(_id)s from %(_class)s with session id %(session_id)s.",
        {"_id": db.id, "_class": db.__class__.__name__, "session_id": id(session)}
    )
    insert_stmt = insert(db_class).values(
        {
            col.key: getattr(db, col.key)
            for col in inspect(db_class).columns
        }
    )
    upsert_stmt = insert_stmt.on_conflict_do_update(
        constraint=on_constraint,
        set_=
        {
            **fields_to_update,
            db_class.modified_at: func.now()  # pylint: disable=not-callable
        }
    )
    session.execute(upsert_stmt)
    if commit:
        session.commit()


def delete_entry(session: Session, _class: Type[T], _id: UUID, commit: bool = True) -> None:
    logger.info(
        "Using generic database request to delete %(_id)s from %(_class)s with session id %(session_id)s.",
        {"_id": _id, "_class": _class, "session_id": id(session)}
    )
    statement = select(_class).where(_class.id == _id)
    result = session.scalars(statement).one_or_none()
    try:
        session.delete(result)
        if commit:
            session.commit()
    except UnmappedInstanceError as exc:
        raise EntryNotFoundError(
            f"Table '{_class.__tablename__}' has no entry with id '{_id}'."
        ) from exc
