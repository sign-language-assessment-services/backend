import logging
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.mappers.multiple_choice_mapper import multiple_choice_to_db, multiple_choice_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry

logger = logging.getLogger(__name__)


def add_multiple_choice(session: Session, multiple_choice: MultipleChoice) -> None:
    db_model = multiple_choice_to_db(multiple_choice)
    for association in db_model.associations:
        session.add(association)
    logger.info(
        "Requesting add multiple choice %(_id)s with session id %(session_id)s.",
        {"_id": db_model.id, "session_id": id(session)}
    )
    add_entry(session, db_model)


def get_multiple_choice(session: Session, _id: UUID) -> MultipleChoice | None:
    logger.info(
        "Requesting multiple choice %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    result = get_by_id(session, DbMultipleChoice, _id)
    if result:
        return multiple_choice_to_domain(result)
    return None


def list_multiple_choices(session: Session) -> list[MultipleChoice]:
    logger.info(
        "Requesting all multiple choices with session id %(session_id)s.",
        {"session_id": id(session)}
    )
    results = get_all(session, DbMultipleChoice)
    return [multiple_choice_to_domain(result) for result in results]


def update_multiple_choice(session: Session, _id: UUID, **kwargs: Any) -> None:
    logger.info(
        "Requesting update multiple choice %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    update_entry(session, DbMultipleChoice, _id, **kwargs)


def delete_multiple_choice(session: Session, _id: UUID) -> None:
    logger.info(
        "Requesting delete multiple choice %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    delete_entry(session, DbMultipleChoice, _id)
