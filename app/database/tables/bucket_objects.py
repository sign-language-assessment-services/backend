from __future__ import annotations

from sqlalchemy import Enum, String, Unicode, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.media_types import MediaType
from app.database.tables.base import DbBase


class DbBucketObjects(DbBase):
    __tablename__ = "bucket_objects"

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
    content_type: Mapped[MediaType] = mapped_column(
        Enum(MediaType),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    choices: Mapped[list["DbChoice"]] = relationship(
        back_populates="bucket_object"
    )
    exercises: Mapped[list["DbExercise"]] = relationship(
        back_populates="bucket_object"
    )
    primers: Mapped[list["DbPrimer"]] = relationship(
        back_populates="bucket_object"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    __table_args__ = (
        UniqueConstraint("bucket", "key"),
    )
