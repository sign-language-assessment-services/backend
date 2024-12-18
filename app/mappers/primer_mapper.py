from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.core.models.primer import Primer
from app.database.tables.primers import DbPrimer


class PrimerMapper:
    @staticmethod
    def db_to_domain(db_primer: DbPrimer) -> Primer:
        return Primer(
            id=db_primer.id,
            created_at=db_primer.created_at,
            content=MultimediaFile(
                id=db_primer.bucket_object.id,
                created_at=db_primer.bucket_object.created_at,
                location=MinioLocation(
                    bucket=db_primer.bucket_object.bucket_object,
                    key=db_primer.bucket_object.key
                ),
                content_type=db_primer.bucket_object.content_type
            )
        )

    @staticmethod
    def domain_to_db(primer: Primer) -> DbPrimer:
        return DbPrimer(
            bucket_id=primer.bucket.id if primer.bucket else None,
            text_id=primer.text.id if primer.text else None
        )
