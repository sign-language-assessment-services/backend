import logging

from app.core.models.choice import AssociatedChoice
from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from app.mappers.choice_mapper import choice_to_domain

logger = logging.getLogger(__name__)


def multiple_choice_to_domain(db_multiple_choice: DbMultipleChoice) -> MultipleChoice:
    logger.debug("Transform DbMultipleChoice into domain model object.")

    choices = [
        AssociatedChoice(
            id=association.choice.id,
            content=choice_to_domain(association.choice).content,
            position=association.position,
            is_correct=association.is_correct
        )
        for association in db_multiple_choice.associations
    ]
    logger.debug(
        "Added %(number)d choices from database object to multiple choices.",
        {"number": len(choices)}
    )

    multiple_choice = MultipleChoice(
        id=db_multiple_choice.id,
        created_at=db_multiple_choice.created_at,
        choices=choices
    )
    return multiple_choice


def multiple_choice_to_db(multiple_choice: MultipleChoice) -> DbMultipleChoice:
    logger.debug("Transform multiple choice into database object.")

    associations = [
        DbMultipleChoicesChoices(
            choice_id=choice.id,
            multiple_choice_id=multiple_choice.id,
            position=choice.position,
            is_correct=choice.is_correct
        )
        for choice in multiple_choice.choices
    ]
    logger.debug(
        "Added %(number)d choices from multiple choice to database object.",
        {"number": len(associations)}
    )

    multiple_choice = DbMultipleChoice(
        id=multiple_choice.id,
        created_at=multiple_choice.created_at,
        associations=associations
    )
    logger.debug(
        "Multiple choice database object with id %(_id)s created.",
        {"_id": multiple_choice.id}
    )
    return multiple_choice
