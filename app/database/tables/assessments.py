from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.database.tables.base import Base


class DbAssessment(Base):
    __tablename__ = "assessments"

    name: Mapped[str] = mapped_column(
        Unicode(length=100),
        nullable=False,
        unique=True
    )

    primers = relationship("DbPrimer", back_populates="assessment")
    exercises = relationship("DbExercise", back_populates="assessment")

    @classmethod
    def from_assessment(cls, assessment: Assessment) -> DbAssessment:
        return cls(
            id=assessment.id,
            created_at=assessment.created_at,
            name=assessment.name,
        )

    def to_assessment(self) -> Assessment:
        return Assessment(
            id=self.id,
            created_at=self.created_at,
            name=self.name,
            items=sorted(primers + exercises, key=lambda item: item.position)
        )

    def to_assessment_summary(self) -> AssessmentSummary:
        return AssessmentSummary(
            id=self.id,
            name=self.name,
        )
