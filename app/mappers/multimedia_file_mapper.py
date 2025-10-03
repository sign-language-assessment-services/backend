import logging

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.bucket_objects import DbBucketObjects

logger = logging.getLogger(__name__)


def bucket_object_to_domain(db_bucket_object: DbBucketObjects) -> MultimediaFile:
    logger.info("Transform DbBucketObject into domain model object.")
    multimedia_file = MultimediaFile(
        id=db_bucket_object.id,
        created_at=db_bucket_object.created_at,
        location=MinioLocation(
            bucket=db_bucket_object.bucket,
            key=db_bucket_object.key
        ),
        media_type=MediaType(db_bucket_object.media_type)
    )
    return multimedia_file


def multimedia_file_to_db(multimedia_file: MultimediaFile) -> DbBucketObjects:
    logger.info("Transform multimedia file into database object.")
    db_bucket_object = DbBucketObjects(
        id=multimedia_file.id,
        created_at=multimedia_file.created_at,
        bucket=multimedia_file.location.bucket,
        key=multimedia_file.location.key,
        media_type=multimedia_file.media_type.value
    )
    logger.info(
        "Bucket object database object with id %(_id)s created.",
        {"_id": db_bucket_object.id}
    )
    return db_bucket_object
