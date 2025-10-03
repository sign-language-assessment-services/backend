import logging
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.bucket_objects import DbBucketObjects
from app.mappers.multimedia_file_mapper import bucket_object_to_domain, multimedia_file_to_db
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry

logger = logging.getLogger(__name__)


def add_multimedia_file(session: Session, multimedia_file: MultimediaFile) -> None:
    db_model = multimedia_file_to_db(multimedia_file)
    logger.info(
        "Requesting add bucket object %(_id)s with session id %(session_id)s.",
        {"_id": db_model.id, "session_id": id(session)}
    )
    add_entry(session, db_model)


def get_multimedia_file(session: Session, _id: UUID) -> MultimediaFile | None:
    logger.info(
        "Requesting bucket object %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    result = get_by_id(session, DbBucketObjects, _id)
    if result:
        return bucket_object_to_domain(result)
    return None


def list_multimedia_files(session: Session) -> list[MultimediaFile]:
    logger.info(
        "Requesting all bucket objects with session id %(session_id)s.",
        {"session_id": id(session)}
    )
    results = get_all(session, DbBucketObjects)
    return [bucket_object_to_domain(result) for result in results]


def update_multimedia_file(session: Session, _id: UUID, **kwargs: Any) -> None:
    logger.info(
        "Requesting update bucket object %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    update_entry(session, DbBucketObjects, _id, **kwargs)


def delete_multimedia_file(session: Session, _id: UUID) -> None:
    logger.info(
        "Requesting delete bucket object %(_id)s with session id %(session_id)s.",
        {"_id": _id, "session_id": id(session)}
    )
    delete_entry(session, DbBucketObjects, _id)
