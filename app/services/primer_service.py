from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.primer import Primer
from app.repositories.primers import get_primer, list_primers
from app.settings import get_settings


class PrimerService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def get_primer_by_id(session: Session, primer_id: UUID) -> Primer | None:
        return get_primer(session=session, _id=primer_id)

    @staticmethod
    def list_primers(session: Session) -> list[Primer]:
        return list_primers(session=session)
