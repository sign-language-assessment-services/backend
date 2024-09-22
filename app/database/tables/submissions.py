from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.submission import Submission
from app.database.tables.base import Base
from app.database.tables.submissions_choices import submission_choice_association


class DbSubmission(Base):
    __tablename__ = "submissions"

    # COLUMNS
    # ------------------------------------------------------------------------
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

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    assessment_id: Mapped[str] = mapped_column(
        ForeignKey(
            "assessments.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    assessment: Mapped["DbAssessment"] = relationship(
        "DbAssessment",
        back_populates="submissions"
    )
    choices: Mapped[list["DbChoice"]] = relationship(
        "DbChoice",
        secondary=submission_choice_association,
        back_populates="submissions"
    )

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
