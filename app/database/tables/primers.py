from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.primer import Primer
from app.database.tables.base import Base


class DbPrimer(Base):
    # pylint: disable=duplicate-code
    __tablename__ = "primers"

    position: Mapped[int] = mapped_column(  # pylint: disable=unsubscriptable-object
        Integer,
        nullable=False
    )

    assessment_id: Mapped[str] = mapped_column(  # pylint: disable=unsubscriptable-object
        ForeignKey("assessments.id"),
        nullable=False
    )

    multimedia_file_id: Mapped[str] = mapped_column(  # pylint: disable=unsubscriptable-object
        ForeignKey("multimedia_files.id"),
        nullable=False
    )

    assessment = relationship("DbAssessment", back_populates="primers")

    UniqueConstraint("position", "assessment_id")

    @classmethod
    def from_primer(cls, primer: Primer) -> DbPrimer:
        return cls(
            id=primer.id,
            created_at=primer.created_at,
            position=primer.position,
            assessment_id=primer.assessment_id,
            multimedia_file_id=primer.multimedia_file_id
        )

    def to_primer(self) -> Primer:
        return Primer(
            id=self.id,
            created_at=self.created_at,
            position=self.position,
            assessment_id=self.assessment_id,
            multimedia_file_id=self.multimedia_file_id
        )
