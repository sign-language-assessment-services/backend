from sqlalchemy.orm import Session

from app.core.models.choice import Choice
from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.choices import DbChoice
from app.database.tables.multiple_choices import DbMultipleChoice
from app.database.tables.multiple_choices_choices import DbMultipleChoicesChoices
from app.repositories.multiple_choices import add_multiple_choice
from tests.database.data_inserts import insert_bucket_object, insert_choice
from tests.database.utils import table_count


def test_association_table_is_correct_after_adding_multiple_choice_with_choices(db_session: Session) -> None:
    multimedia_file = insert_bucket_object(session=db_session)
    choice_1 = Choice(
        **insert_choice(
            session=db_session,
            bucket_object_id=multimedia_file.get("id")),
        is_correct=True
    )
    choice_2 = Choice(
        **insert_choice(
            session=db_session,
            bucket_object_id=multimedia_file.get("id")),
        is_correct=False
    )
    choice_3 = Choice(
        **insert_choice(
            session=db_session,
            bucket_object_id=multimedia_file.get("id")),
        is_correct=False
    )
    multiple_choice = MultipleChoice(choices=[choice_1, choice_2, choice_3])
    add_multiple_choice(session=db_session, multiple_choice=multiple_choice)

    db_choice_1 = db_session.get(DbChoice, choice_1.id)
    db_choice_2 = db_session.get(DbChoice, choice_2.id)
    db_choice_3 = db_session.get(DbChoice, choice_3.id)

    assert db_choice_1.associations[0].position == 1
    assert db_choice_2.associations[0].position == 2
    assert db_choice_3.associations[0].position == 3
    assert db_choice_1.associations[0].is_correct is True
    assert db_choice_2.associations[0].is_correct is False
    assert db_choice_3.associations[0].is_correct is False
    assert table_count(db_session, DbChoice) == 3
    assert table_count(db_session, DbMultipleChoice) == 1
    assert table_count(db_session, DbMultipleChoicesChoices) == 3
