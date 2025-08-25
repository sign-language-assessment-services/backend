from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.multiple_choice import MultipleChoice
from app.repositories.multiple_choices import (
    add_multiple_choice, get_multiple_choice, list_multiple_choices
)
from app.services.choice_service import ChoiceService
from app.settings import get_settings


class MultipleChoiceService:
    def __init__(
            self,
            settings: Annotated[Settings, Depends(get_settings)],
            choice_service: Annotated[ChoiceService, Depends()]
    ):
        self.settings = settings
        self.choice_service = choice_service

    def create_multiple_choice(self, session: Session, choices: list[UUID]) -> None:
        choices = [
            self.choice_service.get_choice_by_id(session=session, choice_id=_id)
            for _id in choices
        ]
        multiple_choice = MultipleChoice(choices=choices)
        add_multiple_choice(session=session, multiple_choice=multiple_choice)

    @staticmethod
    def get_multiple_choice_by_id(session: Session, multpile_choice_id: UUID) -> MultipleChoice | None:
        return get_multiple_choice(session=session, _id=multpile_choice_id)

    @staticmethod
    def list_multiple_choices(session: Session) -> list[MultipleChoice]:
        return list_multiple_choices(session=session)
