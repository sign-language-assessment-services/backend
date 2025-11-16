from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.models.choice import Choice
from app.repositories.choices import add_choice, get_choice, list_choices
from app.services.exceptions.not_found import ChoiceNotFoundException
from app.services.multimedia_file_service import MultimediaFileService


class ChoiceService:
    def __init__(self, multimedia_file_service: Annotated[MultimediaFileService, Depends()]) -> None:
        self.multimedia_file_service = multimedia_file_service

    def create_choice(self, session: Session, multimedia_file_id: UUID) -> Choice:
        multimedia_file = self.multimedia_file_service.get_multimedia_file_by_id(
            session=session,
            multimedia_file_id=multimedia_file_id
        )
        choice = Choice(content=multimedia_file)
        add_choice(session=session, choice=choice)
        return choice

    @staticmethod
    def get_choice_by_id(session: Session, choice_id: UUID) -> Choice | None:
        if result := get_choice(session=session, _id=choice_id):
            return result
        raise ChoiceNotFoundException(f"Choice with id '{choice_id}' not found.")

    @staticmethod
    def list_choices(session: Session) -> list[Choice]:
        return list_choices(session=session)
