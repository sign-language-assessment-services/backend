from datetime import datetime

from sqlalchemy import Float, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.submission import Submission
from app.database.tables.base import Base
from app.database.tables.choices import Choice
from app.database.tables.submissions_choices import submission_choice


class DbSubmission(Base):
    __tablename__ = "submissions"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )

    user_id: Mapped[str] = mapped_column(
        String(length=36),
        nullable=False
    )
    points: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    maximum_points: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id"),
        nullable=False
    )

    choices: Mapped[list[Choice]] = relationship(secondary=submission_choice)

    @classmethod
    def from_submission(cls, submission: Submission) -> "DbSubmission":
        return cls(
            id=submission.id,
            created_at=submission.created_at,
            user_id=submission.user_id,
            points=submission.points,
            maximum_points=submission.maximum_points,
            percentage=submission.percentage,
            assessment_id=submission.assessment_id
        )

    def to_submission(self):
        return Submission(
            id=self.id,
            created_at=self.created_at,
            user_id=self.user_id,
            points=self.points,
            maximum_points=self.maximum_points,
            percentage=self.percentage,
            assessment_id=self.assessment_id,
            answers=self.choices  # todo: rename submissions answers to choices
        )

# TODO: 1. new database creation
#       2. alembic / make database migration possible (after other todos listed here)
#
# TODO: code changes to reflect db changes
#       1. Use submissions_choices n:m table instead of answers column JSON (DONE)
#       2. Create mappings Domain models <-> Database models
