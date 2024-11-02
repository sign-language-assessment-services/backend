from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase
from app.database.tables.multiple_choice_submissions_choices import submissions_choices


class DbChoice(DbBase):
    __tablename__ = "choices"

    # COLUMNS
    # ------------------------------------------------------------------------
    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    bucket_id: Mapped[UUID] = mapped_column(
        ForeignKey("buckets.id"),
        nullable=True
    )
    text_id: Mapped[UUID] = mapped_column(
        ForeignKey("texts.id"),
        nullable=True
    )
    multiple_choice_id: Mapped[UUID] = mapped_column(
        ForeignKey("multiple_choices.id")
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    bucket: Mapped["DbBucket"] = relationship(
        back_populates="choices"
    )
    multiple_choice: Mapped["DbMultipleChoice"] = relationship(
        back_populates="choices"
    )
    text: Mapped["DbText"] = relationship(
        back_populates="choices"
    )

    multiple_choice_submissions: Mapped[list["DbMultipleChoiceSubmission"]] = relationship(
        secondary=submissions_choices,
        back_populates="choices"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    __table_args__ = (
        UniqueConstraint(
            "multiple_choice_id",
            "position"
        ),
        CheckConstraint(
            "text_id IS NOT NULL AND bucket_id IS NULL"
            " OR "
            "text_id IS NULL AND bucket_id IS NOT NULL",
            name='check_choice_text_or_bucket'
        )
    )
