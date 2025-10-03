import logging

from app.core.models.choice import AssociatedChoice
from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from app.mappers.choice_mapper import choice_to_domain

logger = logging.getLogger(__name__)


def multiple_choice_to_domain(db_multiple_choice: DbMultipleChoice) -> MultipleChoice:
    logger.info("Transform DbMultipleChoice into domain model object.")
    
    number = 0
    choices = []
    for association in enumerate(db_multiple_choice.associations, start=1):
        if association.multiple_choice_id == db_multiple_choice.id:  # TODO: better way?
            associated_choice = AssociatedChoice(
                    id=association.choice.id,
                    content=choice_to_domain(association.choice).content,
                    position=association.position,
                    is_correct=association.is_correct
                )
            choices.append(associated_choice)
    logger.info(
        "Added %(number)d choices from database object to multiple choices.",
        {"number": number}
    )

    multiple_choice = MultipleChoice(
        id=db_multiple_choice.id,
        created_at=db_multiple_choice.created_at,
        choices=choices
    )
    return multiple_choice


def multiple_choice_to_db(multiple_choice: MultipleChoice) -> DbMultipleChoice:
    logger.info("Transform multiple choice into database object.")

    number = 0
    associations = []
    for number, choice in enumerate(multiple_choice.choices, start=1):
        db_multiple_choices_choice = DbMultipleChoicesChoices(
                choice_id=choice.id,
                multiple_choice_id=multiple_choice.id,
                position=choice.position,
                is_correct=choice.is_correct
            )
        associations.append(db_multiple_choices_choice)
    logger.info(
        "Added %(number)d choices from multiple choice to database object.",
        {"number": number}
    )

    multiple_choice = DbMultipleChoice(
        id=multiple_choice.id,
        created_at=multiple_choice.created_at,
        associations=associations
    )
    logger.info(
        "Multiple choice database object with id %(_id)s created.",
        {"_id": multiple_choice.id}
    )
    return multiple_choice
