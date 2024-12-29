from typing import Any, Iterable, Type, TypeVar
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.orm import DeclarativeBase, InstrumentedAttribute, Session

from app.database.exceptions import EntryNotFoundError

T = TypeVar("T", bound=DeclarativeBase)


def add_entry(session: Session, db: T) -> None:
    session.add(db)
    session.commit()


def get_by_id(session: Session, _class: Type[T], _id: UUID) -> T | None:
    return session.execute(select(_class).filter_by(id=_id)).unique().scalar_one_or_none()


def get_all(session: Session, _class: Type[T], filter_by: dict[InstrumentedAttribute, Any] = None) -> Iterable[T]:
    query = select(_class)
    if filter_by:
        conditions = [key == value for key, value in filter_by.items()]
        query = query.where(and_(*conditions))
    return session.execute(query).unique().scalars().all()


def update_entry(session: Session, _class: Type[T], _id: UUID, **kwargs) -> None:
    session.execute(update(_class).where(_class.id == _id).values(**kwargs))
    session.commit()


def delete_entry(session: Session, _class: Type[T], _id: UUID) -> None:
    entry = session.get(_class, _id)
    if entry is None:
        raise EntryNotFoundError(
            f"Table '{_class.__tablename__}' has no entry with id '{_id}'."
        )
    session.delete(entry)
    session.commit()