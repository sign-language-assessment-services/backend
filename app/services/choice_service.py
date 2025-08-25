from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.choice import Choice
from app.repositories.choices import add_choice, get_choice, list_choices
from app.services.multimedia_file_service import MultimediaFileService
from app.settings import get_settings


class ChoiceService:
    def __init__(
            self,
            settings: Annotated[Settings, Depends(get_settings)],
            multimedia_file_service: Annotated[MultimediaFileService, Depends()]
    ):
        self.settings = settings
        self.multimedia_file_service = multimedia_file_service

    def create_choice(self, session: Session, multimedia_file_id: UUID, is_correct: bool) -> None:
        multimedia_file = self.multimedia_file_service.get_multimedia_file_by_id(
            session=session,
            multimedia_file_id=multimedia_file_id
        )
        choice = Choice(
            is_correct=is_correct,
            content=multimedia_file
        )
        add_choice(session=session, choice=choice)

    @staticmethod
    def get_choice_by_id(session: Session, choice_id: UUID) -> Choice | None:
        return get_choice(session=session, _id=choice_id)

    @staticmethod
    def list_choices(session: Session) -> list[Choice]:
        return list_choices(session=session)
