from __future__ import annotations

from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.database.tables.base import Base


class DbAssessment(Base):
    __tablename__ = "assessments"

    # COLUMNS
    # ------------------------------------------------------------------------
    name: Mapped[str] = mapped_column(
        Unicode(length=100),
        nullable=False,
        unique=True  # TODO: to be discussed
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    primers: Mapped[list["DbPrimer"]] = relationship(
        "DbPrimer",
        back_populates="assessment",
        cascade="all, delete-orphan"
    )
    exercises: Mapped[list["DbExercise"]] = relationship(
        "DbExercise",
        back_populates="assessment",
        cascade="all, delete-orphan"
    )
    submissions: Mapped[list["DbSubmission"]] = relationship(
        "DbSubmission",
        back_populates="assessment",
        cascade="all, delete-orphan"
    )

    @classmethod
    def from_assessment(cls, assessment: Assessment) -> DbAssessment:
        return cls(
            id=assessment.id,
            created_at=assessment.created_at,
            name=assessment.name,
        )

    def to_assessment(self) -> Assessment:
        primers = [primer.to_primer() for primer in self.primers]
        exercises = [exercise.to_multiple_choice() for exercise in self.exercises]
        items = sorted(primers + exercises, key=lambda item: item.position)
        return Assessment(
            id=self.id,
            created_at=self.created_at,
            name=self.name,
            items=items
        )

    def to_assessment_summary(self) -> AssessmentSummary:
        return AssessmentSummary(
            id=self.id,
            name=self.name,
        )
