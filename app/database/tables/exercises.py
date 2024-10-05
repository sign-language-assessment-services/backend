from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.multiple_choice import MultipleChoice
from app.database.tables.base import Base


class DbExercise(Base):
    __tablename__ = "exercises"

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
        nullable=False
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    assessment: Mapped["DbAssessment"] = relationship(
        "DbAssessment",
        back_populates="exercises"
    )
    choices: Mapped[list["DbChoice"]] = relationship(
        "DbChoice",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )
    multimedia_file = relationship(
        "DbMultiMediaFile",
        back_populates="exercise",
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    UniqueConstraint("position", "assessment_id")

    @classmethod
    def from_multiple_choie(cls, multiple_choice: MultipleChoice) -> DbExercise:
        return cls(
            id=multiple_choice.id,
            created_at=multiple_choice.created_at,
            position=multiple_choice.position,
            assessment_id=multiple_choice.assessment_id,
            multimedia_file_id=multiple_choice.multimedia_file_id
        )

    def to_multiple_choice(self) -> MultipleChoice:
        return MultipleChoice(
            id=self.id,
            created_at=self.created_at,
            position=self.position,
            question=self.multimedia_file.to_multimedia_file(),
            choices=[choice.to_choice() for choice in self.choices],
            assessment_id=self.assessment_id,
            multimedia_file_id=self.multimedia_file_id
        )
