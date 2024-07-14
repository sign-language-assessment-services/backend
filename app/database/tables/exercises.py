from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.exercise import Exercise
from app.database.tables.base import Base


class DbExercise(Base):
    # pylint: disable=duplicate-code
    __tablename__ = "exercises"

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    assessment_id: Mapped[str] = mapped_column(
        ForeignKey("assessments.id"),
        nullable=False
    )
    multimedia_file_id: Mapped[str] = mapped_column(
        ForeignKey("multimedia_files.id"),
        nullable=False
    )

    assessment = relationship("DbAssessment", back_populates="exercises")

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
            assessment_id=self.assessment_id,
            multimedia_file_id=self.multimedia_file_id
        )
