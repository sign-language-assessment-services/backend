from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.buckets import DbBucket


class MultimediaFileMapper:
    @staticmethod
    def db_to_domain(db_bucket: DbBucket) -> MultimediaFile:
        return MultimediaFile(
            id=db_bucket.id,
            created_at=db_bucket.created_at,
            location=MinioLocation(
                bucket=db_bucket.bucket,
                key=db_bucket.key
            ),
            content_type=db_bucket.content_type
        )

    @staticmethod
    def domain_to_db(multimedia_file: MultimediaFile) -> DbBucket:
        return DbBucket(
            bucket=multimedia_file.location.bucket,
            key=multimedia_file.location.key,
            content_type=multimedia_file.content_type
        )
