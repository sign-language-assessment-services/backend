from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.primer import Primer
from app.database.tables.base import Base


class DbPrimer(Base):
    __tablename__ = "primers"

    # COLUMNS
    # ------------------------------------------------------------------------
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "assessments.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    multimedia_file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "multimedia_files.id",
            ondelete="CASCADE"
        ),
        nullable=False,
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    assessment: Mapped["DbAssessment"] = relationship(
        "DbAssessment",
        back_populates="primers"
    )
    multimedia_file: Mapped["DbMultiMediaFile"] = relationship(
        "DbMultiMediaFile",
        back_populates="primer"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    UniqueConstraint("position", "assessment_id")

    @classmethod
    def from_primer(cls, primer: Primer) -> DbPrimer:
        return cls(
            position=primer.position,
            assessment_id=primer.assessment_id,
            multimedia_file_id=primer.multimedia_file_id
        )

    def to_primer(self) -> Primer:
        return Primer(
            id=self.id,
            created_at=self.created_at,
            position=self.position,
            content=self.multimedia_file.to_multimedia_file(),
            assessment_id = self.assessment_id,
            multimedia_file_id = self.multimedia_file_id
        )
