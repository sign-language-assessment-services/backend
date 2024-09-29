from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import Enum, String, Unicode, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_file import MultimediaFile
from app.database.tables.base import Base


class DbMultiMediaFile(Base):
    __tablename__ = "multimedia_files"

    # COLUMNS
    # ------------------------------------------------------------------------
    bucket: Mapped[str] = mapped_column(
        String(length=63),
        nullable=False
    )
    key: Mapped[str] = mapped_column(
        Unicode(length=1024),
        nullable=False
    )
    mediatype: Mapped[MediaType] = mapped_column(
        Enum(MediaType),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    choice: Mapped["DbChoice"] = relationship(
        "DbChoice",
        back_populates="multimedia_file",
        uselist=False
    )
    exercise: Mapped["DbExercise"] = relationship(
        "DbExercise",
        back_populates="multimedia_file",
        uselist=False
    )
    primer: Mapped["DbPrimer"] = relationship(
        "DbPrimer",
        back_populates="multimedia_file",
        uselist=False
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    UniqueConstraint("bucket", "key")

    @classmethod
    def from_multimedia_file(cls, multimedia_file: MultimediaFile) -> DbMultiMediaFile:
        return cls(
            id=str(uuid.uuid4()),
            created_at=datetime.now(tz=timezone.utc),
            bucket=multimedia_file.location.bucket,
            key=multimedia_file.location.key
        )

    def to_multimedia_file(self) -> MultimediaFile:
        return MultimediaFile(
            location=MinioLocation(
                bucket=self.bucket,
                key=self.key
            ),
            type=self.mediatype,
        )
