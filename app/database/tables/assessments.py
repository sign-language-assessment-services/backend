from datetime import datetime

from sqlalchemy import TIMESTAMP, Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.base import DbBase


class DbAssessment(DbBase):
    __tablename__ = "assessments"

    # COLUMNS
    # ------------------------------------------------------------------------
    name: Mapped[str] = mapped_column(
        Unicode(length=100),
        nullable=False
    )
    deadline: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        default=None
    )
    max_attempts: Mapped[int] = mapped_column(
        nullable=True,
        default=None
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    assessment_submissions: Mapped[list["DbAssessmentSubmission"]] = relationship(
        back_populates="assessment"
    )
    tasks: Mapped[list["DbTask"]] = relationship(
        secondary="assessments_tasks",
        back_populates="assessments"
    )
