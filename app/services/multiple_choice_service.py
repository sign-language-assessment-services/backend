from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.models.choice import AssociatedChoice
from app.core.models.multiple_choice import MultipleChoice
from app.repositories.multiple_choices import (
    add_multiple_choice, get_multiple_choice, list_multiple_choices
)
from app.services.choice_service import ChoiceService
from app.services.exceptions.not_found import MultipleChoiceNotFoundException


class MultipleChoiceService:
    def __init__(
            self,
            choice_service: Annotated[ChoiceService, Depends()]
    ):
        self.choice_service = choice_service

    def create_multiple_choice(
            self,
            session: Session,
            choice_ids: list[UUID],
            correct_choice_ids: list[UUID]
    ) -> MultipleChoice:
        multiple_choice = MultipleChoice(
            choices=[
                AssociatedChoice(
                    **self.choice_service.get_choice_by_id(
                        session=session,
                        choice_id=choice_id
                    ).__dict__,
                    position=position,
                    is_correct=choice_id in correct_choice_ids
                )
                for position, choice_id in enumerate(choice_ids, start=1)
            ]
        )
        add_multiple_choice(session=session, multiple_choice=multiple_choice)

        return multiple_choice

    @staticmethod
    def get_multiple_choice_by_id(session: Session, multiple_choice_id: UUID) -> MultipleChoice | None:
        if result := get_multiple_choice(session=session, _id=multiple_choice_id):
            return result
        raise MultipleChoiceNotFoundException(f"Multiple choice with id '{multiple_choice_id}' not found.")

    @staticmethod
    def list_multiple_choices(session: Session) -> list[MultipleChoice]:
        return list_multiple_choices(session=session)
