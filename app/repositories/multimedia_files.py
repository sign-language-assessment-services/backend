from typing import Any

from sqlalchemy.orm import Session

from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.buckets import DbBucket
from app.mappers.multimedia_file_mapper import MultimediaFileMapper


def add_multimedia_file(session: Session, multimedia_file: MultimediaFile) -> None:
    db_model = MultimediaFileMapper.domain_to_db(multimedia_file)
    session.add(db_model)
    session.commit()
    return None


def get_multimedia_file_by_id(session: Session, _id: str) -> MultimediaFile | None:
    result = session.get(DbBucket, {"id": _id})
    if result:
        model = MultimediaFileMapper.db_to_domain(result)
        return model
    return None


def list_multimedia_files(session: Session) -> list[MultimediaFile]:
    results = session.query(DbBucket).all()
    models = [MultimediaFileMapper.db_to_domain(result) for result in results]
    return models


def update_multimedia_file(session: Session, multimedia_file: MultimediaFile, **kwargs: dict[str, Any]) -> None:
    session.query(DbBucket).filter_by(id=multimedia_file.id).update(kwargs)
    session.commit()
    return None


def delete_multimedia_file_by_id(session: Session, _id: str) -> None:
    session.query(DbBucket).filter_by(id=_id).delete()
    session.commit()
    return None
