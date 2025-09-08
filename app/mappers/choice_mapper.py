from app.core.models.choice import AssociatedChoice, Choice
from app.database.tables.choices import DbChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from app.mappers.multimedia_file_mapper import bucket_object_to_domain


def choice_to_domain(db_choice: DbChoice) -> Choice:
    return Choice(
        id=db_choice.id,
        created_at=db_choice.created_at,
        content=bucket_object_to_domain(db_choice.bucket_object),
    )


def choice_to_db(choice: Choice | AssociatedChoice) -> DbChoice:
    db_choice = DbChoice(
        id=choice.id,
        created_at=choice.created_at,
        bucket_object_id=choice.content.id,
    )
    if isinstance(choice, AssociatedChoice):
        db_choice.associations = [
            DbMultipleChoicesChoices(
                choice_id=choice.id,
                multiple_choice_id=association.multiple_choice_id,
                position=association.position,
                is_correct=association.is_correct
            )
            for association in choice.multiple_choices
        ]
    return db_choice
