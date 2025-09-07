from app.core.models.choice import Choice, MultipleChoiceUsage
from app.database.tables.choices import DbChoice
from app.mappers.multimedia_file_mapper import bucket_object_to_domain


def choice_to_domain(db_choice: DbChoice) -> Choice:
    return Choice(
        id=db_choice.id,
        created_at=db_choice.created_at,
        content=bucket_object_to_domain(db_choice.bucket_object),
        multiple_choices=_get_usages_in_multiple_choices(db_choice)
    )


def choice_to_db(choice: Choice) -> DbChoice:
    return DbChoice(
        id=choice.id,
        created_at=choice.created_at,
        bucket_object_id=choice.content.id
    )


def _get_usages_in_multiple_choices(db_choice: DbChoice) -> list[MultipleChoiceUsage]:
    return [
        MultipleChoiceUsage(
            id=choice.multiple_choice.id,
            position=choice.position
        )
        for choice in db_choice.associations
        if choice.choice_id == db_choice.id
    ]
