from uuid import UUID

from sqlalchemy import Float, ForeignKey, UniqueConstraint, Uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase


class DbExerciseSubmission(DbBase):
    __tablename__ = "exercise_submissions"

    # COLUMNS
    # ------------------------------------------------------------------------
    user_id: Mapped[UUID] = mapped_column(
        nullable=False
    )
    choices: Mapped[list[UUID]] = mapped_column(
        MutableList.as_mutable(ARRAY(Uuid, dimensions=1)),
        nullable=True
    )
    score: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    assessment_submission_id: Mapped[UUID] = mapped_column(
        ForeignKey("assessment_submissions.id"),
        nullable=False
    )
    exercise_id: Mapped[UUID] = mapped_column(
        ForeignKey("exercises.id"),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    assessment_submission: Mapped["DbAssessmentSubmission"] = relationship(
        back_populates="exercise_submissions"
    )
    exercise: Mapped["DbExercise"] = relationship(
        back_populates="exercise_submissions"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    __table_args__ = (
        UniqueConstraint("assessment_submission_id", "exercise_id"),
    )
