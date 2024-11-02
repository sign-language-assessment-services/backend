from __future__ import annotations

from sqlalchemy import Enum, String, Unicode, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.media_types import MediaType
from app.database.tables.base import DbBase


class DbBucket(DbBase):
    __tablename__ = "buckets"

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
        back_populates="bucket"
    )
    exercises: Mapped[list["DbExercise"]] = relationship(
        back_populates="bucket"
    )
    primers: Mapped[list["DbPrimer"]] = relationship(
        back_populates="bucket"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    __table_args__ = (
        UniqueConstraint("bucket", "key"),
    )
