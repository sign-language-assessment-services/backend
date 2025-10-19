import logging
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.primer import Primer
from app.database.tables.primers import DbPrimer
from app.mappers.primer_mapper import primer_to_db, primer_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry

logger = logging.getLogger(__name__)


def add_primer(session: Session, primer: Primer) -> None:
    db_model = primer_to_db(primer)
    logger.debug(
        "Requesting add primer %(_id)s with session id %(session_id)s.",
        {"_id": db_model.id, "session_id": id(session)}
    )
    add_entry(session, db_model)


def get_primer(session: Session, _id: UUID) -> Primer | None:
    logger.debug(
        "Requesting primer %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    result = get_by_id(session, DbPrimer, _id)
    if result:
        return primer_to_domain(result)
    return None


def list_primers(session: Session) -> list[Primer]:
    logger.debug(
        "Requesting all primers with session id %(session_id)s.",
        {"session_id": id(session)}
    )
    results = get_all(session, DbPrimer)
    return [primer_to_domain(result) for result in results]


def update_primer(session: Session, _id: UUID, **kwargs: Any) -> None:
    logger.debug(
        "Requesting update primer %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    update_entry(session, DbPrimer, _id, **kwargs)


def delete_primer(session: Session, _id: UUID) -> None:
    logger.debug(
        "Requesting delete primer %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    delete_entry(session, DbPrimer, _id)
