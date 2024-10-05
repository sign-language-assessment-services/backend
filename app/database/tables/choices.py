from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_choice import MultimediaChoice
from app.database.tables.base import Base


class DbChoice(Base):
    __tablename__ = "choices"

    # COLUMNS
    # ------------------------------------------------------------------------
    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    exercise_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "exercises.id",
            ondelete="CASCADE"
        ),
        nullable=False,
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
    exercise: Mapped["DbExercise"] = relationship(
        "DbExercise",
        back_populates="choices"
    )
    multimedia_file: Mapped["DbMultiMediaFile"] = relationship(
        "DbMultiMediaFile",
        back_populates="choice",
    )
    submissions: Mapped[list["DbSubmission"]] = relationship(
        "DbSubmission",
        secondary="submissions_choices",
        back_populates="choices"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    UniqueConstraint("exercise_id", "multimedia_file_id")


    @classmethod
    def from_choice(cls, choice: MultimediaChoice) -> DbChoice:
        return cls(
            id=choice.id,
            created_at=choice.created_at,
            is_correct=choice.is_correct,
            exercise_id=choice.exercise_id,
            multimedia_file_id=choice.multimedia_file_id
        )

    def to_choice(self) -> MultimediaChoice:
        return MultimediaChoice(
            id=self.id,
            created_at=self.created_at,
            location=MinioLocation(
                bucket=self.multimedia_file.to_multimedia_file().location.bucket,
                key=self.multimedia_file.to_multimedia_file().location.key
            ),
            is_correct=self.is_correct,
            exercise_id=self.exercise_id,
            multimedia_file_id=self.multimedia_file_id,
            type=MediaType.VIDEO
        )
