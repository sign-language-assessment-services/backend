from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.tasks import DbTask
from app.database.type_hints import Bucket, MultipleChoice, Text


class DbExercise(DbTask):
    __tablename__ = "exercises"

    # FOREIGN_KEYS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True
    )
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
        back_populates="exercises"
    )
    multiple_choice: Mapped[MultipleChoice] = relationship(
        back_populates="exercises"
    )
    text: Mapped[Text] = relationship(
        back_populates="exercises"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    CheckConstraint(
        "text_id IS NOT NULL AND bucket_id IS NULL"
        " OR "
        "text_id IS NULL AND bucket_id IS NOT NULL",
        name="check_exercise_text_or_bucket"
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_identity": "exercise"
    }
