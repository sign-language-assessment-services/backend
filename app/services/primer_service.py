from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.models.primer import Primer
from app.repositories.primers import add_primer, get_primer, list_primers
from app.services.multimedia_file_service import MultimediaFileService


class PrimerService:
    def __init__(
            self,
            multimedia_file_service: Annotated[MultimediaFileService, Depends()]
    ):
        self.multimedia_file_service = multimedia_file_service

    def create_primer(self, session: Session, multimedia_file_id: UUID) -> Primer:
        multimedia_file = self.multimedia_file_service.get_multimedia_file_by_id(
            session=session,
            multimedia_file_id=multimedia_file_id
        )
        primer = Primer(content=multimedia_file)
        add_primer(session=session, primer=primer)
        return primer

    @staticmethod
    def get_primer_by_id(session: Session, primer_id: UUID) -> Primer | None:
        return get_primer(session=session, _id=primer_id)

    @staticmethod
    def list_primers(session: Session) -> list[Primer]:
        return list_primers(session=session)
