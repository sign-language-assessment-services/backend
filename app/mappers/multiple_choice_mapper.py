from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.mappers.choice_mapper import ChoiceMapper


class MultipleChoiceMapper:
    @staticmethod
    def db_to_domain(db_multiple_choice: DbMultipleChoice) -> MultipleChoice:
        return MultipleChoice(
            id=db_multiple_choice.id,
            created_at=db_multiple_choice.created_at,
            choices=[ChoiceMapper.db_to_domain(choice) for choice in db_multiple_choice.choices],
            random_order=db_multiple_choice.random
        )

    @staticmethod
    def domain_to_db(multiple_choice: MultipleChoice) -> DbMultipleChoice:
        return DbMultipleChoice(
            choices=multiple_choice.choices,
            random=multiple_choice.random_order
        )
