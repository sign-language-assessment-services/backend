from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.submission import Submission
from app.database.tables.base import Base
from app.database.tables.choices import DbChoice
from app.database.tables.submissions_choices import submission_choice


class DbSubmission(Base):
    __tablename__ = "submissions"

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

    choices: Mapped[list[DbChoice]] = relationship(secondary=submission_choice)

    @classmethod
    def from_submission(cls, submission: Submission) -> DbSubmission:
        return cls(
            id=submission.id,
            created_at=submission.created_at,
            user_id=submission.user_id,
            points=submission.points,
            maximum_points=submission.maximum_points,
            percentage=submission.percentage,
            assessment_id=submission.assessment_id
        )

    def to_submission(self) -> Submission:
        return Submission(
            id=self.id,
            created_at=self.created_at,
            user_id=self.user_id,
            points=self.points,
            maximum_points=self.maximum_points,
            percentage=self.percentage,
            assessment_id=self.assessment_id,
            answers=[db_choice.to_choice() for db_choice in self.choices]
        )
