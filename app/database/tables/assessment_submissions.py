from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey
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
