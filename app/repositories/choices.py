from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.choice import Choice
from app.database.tables.choices import DbChoice
from app.mappers.choice_mapper import choice_to_db, choice_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry


def add_choice(session: Session, choice: Choice) -> None:
    db_model = choice_to_db(choice)
    add_entry(session, db_model)


def get_choice(session: Session, _id: UUID) -> Choice | None:
    result = get_by_id(session, DbChoice, _id)
    if result:
        return choice_to_domain(result)


def list_choices(session: Session) -> list[Choice]:
    results = get_all(session, DbChoice)
    return [choice_to_domain(result) for result in results]


def update_choice(session: Session, _id: UUID, **kwargs: Any) -> None:
    update_entry(session, DbChoice, _id, **kwargs)


def delete_choice(session: Session, _id: UUID) -> None:
    delete_entry(session, DbChoice, _id)
