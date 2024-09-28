from sqlalchemy.orm import Session

from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.multimedia_files import DbMultiMediaFile


def add_multimedia_file(session: Session, multimedia_file: MultimediaFile) -> None:
    session.add(DbMultiMediaFile.from_multimedia_file(multimedia_file))
    session.commit()


def get_multimedia_file_by_id(session: Session, _id: str) -> MultimediaFile:
    result: DbMultiMediaFile = session.query(DbMultiMediaFile).get({"id": _id})
    return result.to_multimedia_file()


def list_multimedia_files(session: Session) -> list[MultimediaFile]:
    result: DbMultiMediaFile = session.query(DbMultiMediaFile).all()
    return [multimedia_file.to_multimedia_file() for multimedia_file in result]


def delete_multimedia_file_by_id(session: Session, _id: str) -> None:
    session.query(DbMultiMediaFile).filter_by(id=_id).delete()
    session.commit()
