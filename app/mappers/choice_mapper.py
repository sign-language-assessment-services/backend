from app.core.models.choice import Choice
from app.database.tables.choices import DbChoice
from app.mappers.multimedia_file_mapper import bucket_object_to_domain


def choice_to_domain(db_choice: DbChoice) -> Choice:
    return Choice(
        id=db_choice.id,
        created_at=db_choice.created_at,
        content=bucket_object_to_domain(db_choice.bucket_object)
    )


def choice_to_db(choice: Choice) -> DbChoice:
    return DbChoice(
        id=choice.id,
        created_at=choice.created_at,
        bucket_object_id=choice.content.id
    )
