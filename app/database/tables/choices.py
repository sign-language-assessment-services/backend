from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase
from app.database.tables.multiple_choices_choices import multiple_choices_choices


class DbChoice(DbBase):
    __tablename__ = "choices"

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    bucket_object_id: Mapped[UUID] = mapped_column(
        ForeignKey("bucket_objects.id"),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    bucket_object: Mapped["DbBucketObjects"] = relationship(
        back_populates="choices"
    )
    multiple_choices: Mapped[list["DbMultipleChoice"]] = relationship(
        secondary=multiple_choices_choices,
        back_populates="choices"
    )
