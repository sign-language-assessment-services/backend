from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.mappers.choice_mapper import choice_to_db, choice_to_domain


def multiple_choice_to_domain(db_multiple_choice: DbMultipleChoice) -> MultipleChoice:
    return MultipleChoice(
        id=db_multiple_choice.id,
        created_at=db_multiple_choice.created_at,
        choices=[choice_to_domain(c) for c in db_multiple_choice.choices],
    )


def multiple_choice_to_db(multiple_choice: MultipleChoice) -> DbMultipleChoice:
    return DbMultipleChoice(
        id=multiple_choice.id,
        created_at=multiple_choice.created_at,
        choices=[choice_to_db(c) for c in multiple_choice.choices]
    )
