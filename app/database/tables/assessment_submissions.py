from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase


class DbAssessmentSubmission(DbBase):
    __tablename__ = "assessment_submissions"

    # COLUMNS
    # ------------------------------------------------------------------------
    user_id: Mapped[UUID] = mapped_column(
        nullable=False
    )
    score: Mapped[float] = mapped_column(
        nullable=True
    )
    finished: Mapped[bool] = mapped_column(
        nullable=False,
        default=False
    )
    finished_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        default=None
    )

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    assessment_id: Mapped[UUID] = mapped_column(
        ForeignKey("assessments.id"),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    assessment: Mapped["DbAssessment"] = relationship(
        back_populates="assessment_submissions"
    )
    exercise_submissions: Mapped[list["DbExerciseSubmission"]] = relationship(
        back_populates="assessment_submission"
    )

    # CONFIGURATIONS
    # ------------------------------------------------------------------------
    __table_args__ = (
        CheckConstraint(
            "NOT (finished = true AND finished_at IS NULL)",
            name="check_finished_at_only_when_finished"
        ),
    )
