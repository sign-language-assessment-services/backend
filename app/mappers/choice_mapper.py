import logging

from app.core.models.choice import AssociatedChoice, Choice
from app.database.tables.choices import DbChoice
from app.mappers.multimedia_file_mapper import bucket_object_to_domain

logger = logging.getLogger(__name__)


def choice_to_domain(db_choice: DbChoice) -> Choice:
    logger.debug("Transform DbChoice into domain model object.")
    choice = Choice(
        id=db_choice.id,
        created_at=db_choice.created_at,
        content=bucket_object_to_domain(db_choice.bucket_object),
    )
    return choice


def choice_to_db(choice: Choice | AssociatedChoice) -> DbChoice:
    logger.debug("Transform choice into domain model object.")
    db_choice = DbChoice(
        id=choice.id,
        created_at=choice.created_at,
        bucket_object_id=choice.content.id,
    )
    logger.debug(
        "Choice database object with id %(_id)s created.",
        {"_id": db_choice.id}
    )
    return db_choice
