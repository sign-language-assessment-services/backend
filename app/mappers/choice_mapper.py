import logging

from app.core.models.choice import AssociatedChoice, Choice
from app.database.tables.choices import DbChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from app.mappers.multimedia_file_mapper import bucket_object_to_domain

logger = logging.getLogger(__name__)


def choice_to_domain(db_choice: DbChoice) -> Choice:
    logger.info("Transform DbChoice into domain model object.")
    choice = Choice(
        id=db_choice.id,
        created_at=db_choice.created_at,
        content=bucket_object_to_domain(db_choice.bucket_object),
    )
    return choice


def choice_to_db(choice: Choice | AssociatedChoice) -> DbChoice:
    logger.info("Transform choice into domain model object.")
    db_choice = DbChoice(
        id=choice.id,
        created_at=choice.created_at,
        bucket_object_id=choice.content.id,
    )
    logger.info(
        "Choice database object with id %(_id)s created.",
        {"_id": db_choice.id}
    )

    number = 0
    if isinstance(choice, AssociatedChoice):
        db_choice_associations = []
        for number, association in enumerate(choice.multiple_choices, start=1):
            db_choice_association = DbMultipleChoicesChoices(
                choice_id=choice.id,
                multiple_choice_id=association.multiple_choice_id,
                position=association.position,
                is_correct=association.is_correct
            )
            db_choice_associations.append(db_choice_association)

    logger.info(
        "Added %(number)d choice associations to database object.",
        {"number": number}
    )
    return db_choice
