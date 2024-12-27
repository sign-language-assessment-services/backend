from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.bucket_objects import DbBucketObjects
from app.mappers.multimedia_file_mapper import bucket_object_to_domain, multimedia_file_to_db
from app.repositories.utils import add_entry, delete_entry, get_all, get_by_id, update_entry


def add_multimedia_file(session: Session, multimedia_file: MultimediaFile) -> None:
    db_model = multimedia_file_to_db(multimedia_file)
    add_entry(session, db_model)


def get_multimedia_file(session: Session, _id: UUID) -> MultimediaFile | None:
    result = get_by_id(session, DbBucketObjects, _id)
    if result:
        return bucket_object_to_domain(result)
    return None


def list_multimedia_files(session: Session) -> list[MultimediaFile]:
    results = get_all(session, DbBucketObjects)
    return [bucket_object_to_domain(result) for result in results]


def update_multimedia_file(session: Session, _id: UUID, **kwargs: Any) -> None:
    update_entry(session, DbBucketObjects, _id, **kwargs)


def delete_multimedia_file(session: Session, _id: UUID) -> None:
    delete_entry(session, DbBucketObjects, _id)
