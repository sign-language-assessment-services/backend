from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.tasks import DbTask


class DbExercise(DbTask):
    __tablename__ = "exercises"

    # FOREIGN_KEYS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True
    )
    # bucket or text represents the question
    bucket_id: Mapped[UUID] = mapped_column(
        ForeignKey("buckets.id"),
        nullable=True
    )
    text_id: Mapped[UUID] = mapped_column(
        ForeignKey("texts.id"),
        nullable=True
    )
    # multiple choice is currently the only possibility to answer an exercise
    multiple_choice_id: Mapped[UUID] = mapped_column(
        ForeignKey("multiple_choices.id")
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    submission: Mapped["DbSubmission"] = relationship(
        back_populates="exercise"
    )
    bucket: Mapped["DbBucket"] = relationship(
        back_populates="exercises"
    )
    multiple_choice: Mapped["DbMultipleChoice"] = relationship(
        back_populates="exercises"
    )
    text: Mapped["DbText"] = relationship(
        back_populates="exercises"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    __table_args__ = (
        CheckConstraint(
            "text_id IS NOT NULL AND bucket_id IS NULL"
            " OR "
            "text_id IS NULL AND bucket_id IS NOT NULL",
            name="check_exercise_text_or_bucket"
        ),
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_identity": "exercise"
    }
