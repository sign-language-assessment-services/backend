from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Unicode, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.base import Base


class DbMultiMediaFiles(Base):
    __tablename__ = "multimedia_files"

    bucket: Mapped[str] = mapped_column(
        String(length=63),
        nullable=False
    )
    key: Mapped[str] = mapped_column(
        Unicode(length=1024),
        nullable=False
    )

    UniqueConstraint("bucket", "key")

    @classmethod
    def from_multimedia_file(cls, multimedia_file: MultimediaFile) -> DbMultiMediaFiles:
        return cls(
            id=str(uuid.uuid4()),
            created_at=datetime.now(tz=timezone.utc),
            bucket=multimedia_file.bucket,
            key=multimedia_file.key
        )

    def to_multimedia_file(self) -> MultimediaFile:
        return MultimediaFile(
            bucket=self.bucket,
            key=self.key
        )
