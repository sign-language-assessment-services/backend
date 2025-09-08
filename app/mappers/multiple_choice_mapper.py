from app.core.models.choice import AssociatedChoice
from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from app.mappers.choice_mapper import choice_to_domain


def multiple_choice_to_domain(db_multiple_choice: DbMultipleChoice) -> MultipleChoice:
    return MultipleChoice(
        id=db_multiple_choice.id,
        created_at=db_multiple_choice.created_at,
        choices=[
            AssociatedChoice(
                id=association.choice.id,
                content=choice_to_domain(association.choice).content,
                position=association.position,
                is_correct=association.is_correct
            )
            for association in db_multiple_choice.associations
            if association.multiple_choice_id == db_multiple_choice.id
        ]
    )


def multiple_choice_to_db(multiple_choice: MultipleChoice) -> DbMultipleChoice:
    multiple_choice = DbMultipleChoice(
        id=multiple_choice.id,
        created_at=multiple_choice.created_at,
        associations=[
            DbMultipleChoicesChoices(
                choice_id=choice.id,
                multiple_choice_id=multiple_choice.id,
                position=choice.position,
                is_correct=choice.is_correct
            )
            for choice in multiple_choice.choices
        ]
    )
    return multiple_choice
