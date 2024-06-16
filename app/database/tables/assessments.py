from datetime import datetime

from sqlalchemy import String, TIMESTAMP, Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.assessment import Assessment
from app.core.models.assessment_summary import AssessmentSummary
from app.database.tables.base import Base


class DbAssessment(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        Unicode(length=100),
        nullable=False,
        unique=True
    )

    primers = relationship("DbPrimer", back_populates="assessment")

    @classmethod
    def from_assessment(cls, assessment: Assessment) -> "DbAssessment":
        return cls(
            id=assessment.id,
            created_at=assessment.created_at,
            name=assessment.name,
        )

    def to_assessment(self):
        return Assessment(
            id=self.id,
            created_at=self.created_at,
            name=self.name,
        )

    def to_assessment_summary(self):
        return AssessmentSummary(
            id=self.id,
            name=self.name,
        )
