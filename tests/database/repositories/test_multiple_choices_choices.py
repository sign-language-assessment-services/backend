from sqlalchemy.orm import Session

from app.core.models.choice import Choice
from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.choices import DbChoice
from app.mappers.choice_mapper import choice_to_domain
from app.repositories.multiple_choices import add_multiple_choice
from tests.database.data_inserts import insert_bucket_object


def test_choice_model_has_is_correct_from_association_table(db_session: Session) -> None:
    video_id = insert_bucket_object(session=db_session).get("id")
    choice_content = MultimediaFile(
        id=video_id,
        location=MinioLocation(bucket="1", key="test.mpg"),
        media_type=MediaType.VIDEO
    )
    choice_1 = Choice(content=choice_content, is_correct=True)
    choice_2 = Choice(content=choice_content, is_correct=False)
    choice_3 = Choice(content=choice_content)  # default = False
    multiple_choice = MultipleChoice(choices=[choice_1, choice_2, choice_3])
    add_multiple_choice(session=db_session, multiple_choice=multiple_choice)
    db_choice_1 = db_session.get(DbChoice, choice_1.id)
    db_choice_2 = db_session.get(DbChoice, choice_2.id)
    db_choice_3 = db_session.get(DbChoice, choice_3.id)

    result_1 = choice_to_domain(db_choice_1)
    result_2 = choice_to_domain(db_choice_2)
    result_3 = choice_to_domain(db_choice_3)

    assert result_1.is_correct is True
    assert result_2.is_correct is False
    assert result_3.is_correct is False
