from app.core.models.choice import Choice
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.choices import DbChoice


class ChoiceMapper:
    @staticmethod
    def db_to_domain(db_choice: DbChoice) -> Choice:
        return Choice(
            id=db_choice.id,
            created_at=db_choice.created_at,
            is_correct=db_choice.is_correct,
            position=db_choice.position,
            content=MultimediaFile(
                id=db_choice.bucket_object.id,
                created_at=db_choice.bucket_object.created_at,
                location=MinioLocation(
                    bucket=db_choice.bucket_object.bucket_object,
                    key=db_choice.bucket_object.key
                ),
                content_type=db_choice.bucket_object.content_type
            )
        )

    @staticmethod
    def from_choice(choice: Choice) -> DbChoice:
        return DbChoice(
            is_correct=choice.is_correct,
            position=choice.position,
            bucket_id=choice.bucket.id,
            multiple_choice=choice.multiple_choice.id if choice.multiple_choice else None,
            text_id=choice.text.id if choice.text else None
        )
