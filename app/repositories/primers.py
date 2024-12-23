from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.primer import Primer
from app.database.tables.primers import DbPrimer
from app.mappers.primer_mapper import primer_to_db, primer_to_domain
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry


def add_primer(session: Session, primer: Primer) -> None:
    db_model = primer_to_db(primer)
    add_entry(session, db_model)


def get_primer(session: Session, _id: UUID) -> Primer | None:
    result = get_by_id(session, DbPrimer, _id)
    if result:
        return primer_to_domain(result)


def list_primers(session: Session) -> list[Primer]:
    results = get_all(session, DbPrimer)
    return [primer_to_domain(result) for result in results]


def update_primer(session: Session, _id: UUID, **kwargs: Any) -> None:
    update_entry(session, DbPrimer, _id, **kwargs)


def delete_primer(session: Session, _id: UUID) -> None:
    delete_entry(session, DbPrimer, _id)
