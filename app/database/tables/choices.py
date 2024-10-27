from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase
from app.database.type_hints import Bucket, MultipleChoice, MultipleChoiceSubmissions, Text


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
        ForeignKey("buckets.id")
    )
    multiple_choice_id: Mapped[UUID] = mapped_column(
        ForeignKey("multiple_choices.id")
    )
    text_id: Mapped[UUID] = mapped_column(
        ForeignKey("texts.id")
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    bucket: Mapped[Bucket] = relationship(
        back_populates="choices"
    )
    multiple_choice: Mapped[MultipleChoice] = relationship(
        back_populates="choices"
    )
    text: Mapped[Text] = relationship(
        back_populates="choices"
    )

    multiple_choice_submissions: Mapped[MultipleChoiceSubmissions] = relationship(
        secondary="multiple_choice_submissions_choices",
        back_populates="choices"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    UniqueConstraint("multiple_choice_id", "position")
    CheckConstraint(
        "text_id IS NOT NULL AND id NOT IN (SELECT choice_id FROM choices_buckets)"
        " OR "
        "text_id IS NULL AND id IN (SELECT choice_id FROM choices_buckets)",
        name='check_choice_text_or_bucket'
    )
