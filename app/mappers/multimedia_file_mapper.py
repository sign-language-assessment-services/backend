from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.bucket_objects import DbBucketObjects


class MultimediaFileMapper:
    @staticmethod
    def db_to_domain(db_bucket: DbBucketObjects) -> MultimediaFile:
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
    def domain_to_db(multimedia_file: MultimediaFile) -> DbBucketObjects:
        return DbBucketObjects(
            bucket=multimedia_file.location.bucket,
            key=multimedia_file.location.key,
            content_type=multimedia_file.content_type
        )
