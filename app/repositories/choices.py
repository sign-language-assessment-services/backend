import logging
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.choice import Choice
from app.database.tables.choices import DbChoice
from app.mappers.choice_mapper import choice_to_db, choice_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry

logger = logging.getLogger(__name__)


def add_choice(session: Session, choice: Choice) -> None:
    db_model = choice_to_db(choice)
    logger.debug(
        "Requesting add choice %(_id)s with session id %(session_id)s.",
        {"_id": db_model.id, "session_id": id(session)}
    )
    add_entry(session, db_model)


def get_choice(session: Session, _id: UUID) -> Choice | None:
    logger.debug(
        "Requesting choice %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    result = get_by_id(session, DbChoice, _id)
    if result:
        return choice_to_domain(result)
    return None


def list_choices(session: Session) -> list[Choice]:
    logger.debug(
        "Requesting all choices with session id %(session_id)s.",
        {"session_id": id(session)}
    )
    results = get_all(session, DbChoice)
    return [choice_to_domain(result) for result in results]


def update_choice(session: Session, _id: UUID, **kwargs: Any) -> None:
    logger.debug(
        "Requesting update choice %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    update_entry(session, DbChoice, _id, **kwargs)


def delete_choice(session: Session, _id: UUID) -> None:
    logger.debug(
        "Requesting delete choice %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    delete_entry(session, DbChoice, _id)
