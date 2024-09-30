from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.exercise import Exercise
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
    def from_exercise(cls, exercise: Exercise) -> DbExercise:
        return cls(
            id=exercise.id,
            created_at=exercise.created_at,
            position=exercise.position,
            assessment_id=exercise.assessment_id,
            multimedia_file_id=exercise.multimedia_file_id
        )

    def to_exercise(self) -> Exercise:
        return Exercise(
            id=self.id,
            created_at=self.created_at,
            position=self.position,
            question=self.multimedia_file.to_multimedia_file(),
            choices=[choice.to_choice() for choice in self.choices],
            assessment_id=self.assessment_id,
            multimedia_file_id=self.multimedia_file_id
        )
