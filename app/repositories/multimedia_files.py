from sqlalchemy.orm import Session

from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.multimedia_files import DbMultiMediaFiles


def add_multimedia_file(session: Session, multimedia_file: MultimediaFile) -> None:
    session.add(DbMultiMediaFiles.from_multimedia_file(multimedia_file))
    session.commit()


def get_multimedia_file_by_id(session: Session, _id: str) -> MultimediaFile:
    result = session.query(DbMultiMediaFiles).get({"id": _id})
    return result.to_multimedia_file()


def list_multimedia_files(session: Session) -> list[MultimediaFile]:
    result = session.query(DbMultiMediaFiles).all()
    return [multimedia_file.to_multimedia_file() for multimedia_file in result]


def delete_multimedia_file_by_id(session: Session, _id: str) -> None:
    session.query(DbMultiMediaFiles).filter_by(id=_id).delete()
    session.commit()
