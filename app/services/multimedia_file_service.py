from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import Settings
from app.core.models.multimedia_file import MultimediaFile
from app.repositories.multimedia_files import get_multimedia_file
from app.settings import get_settings


class MultimediaFileService:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        self.settings = settings

    @staticmethod
    def get_multimedia_file_by_id(session: Session, multimedia_file_id: UUID) -> MultimediaFile | None:
        return get_multimedia_file(session=session, _id=multimedia_file_id)
