from app.core.models.choice import Choice
from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from app.mappers.choice_mapper import choice_to_db, choice_to_domain


def multiple_choice_to_domain(db_multiple_choice: DbMultipleChoice) -> MultipleChoice:
    return MultipleChoice(
        id=db_multiple_choice.id,
        created_at=db_multiple_choice.created_at,
        choices=[
            Choice(
                id=association.choice.id,
                content=choice_to_domain(association.choice).content,
                is_correct=association.is_correct
            )
            for association in db_multiple_choice.associations
        ]
    )


def multiple_choice_to_db(multiple_choice: MultipleChoice) -> DbMultipleChoice:
    multiple_choice = DbMultipleChoice(
        id=multiple_choice.id,
        created_at=multiple_choice.created_at,
        associations=[
            DbMultipleChoicesChoices(
                choice=choice_to_db(choice),
                position=pos,
                is_correct=choice.is_correct
            )
            for pos, choice in enumerate(multiple_choice.choices, start=1)
        ]
    )
    return multiple_choice
