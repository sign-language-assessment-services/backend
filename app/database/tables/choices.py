from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.media_types import MediaType
from app.core.models.minio_location import MinioLocation
from app.core.models.multimedia_choice import MultimediaChoice
from app.database.tables.base import Base


class DbChoice(Base):
    __tablename__ = "choices"

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    exercise_id: Mapped[str] = mapped_column(
        ForeignKey("exercises.id"),
        nullable=False
    )
    multimedia_file_id: Mapped[str] = mapped_column(
        ForeignKey("multimedia_files.id"),
        nullable=False
    )

    UniqueConstraint("exercise_id", "multimedia_file_id")

    def to_choice(self) -> MultimediaChoice:
        return MultimediaChoice(
            location=MinioLocation(
                bucket="slportal",
                key=self.multimedia_file_id
            ),
            is_correct=self.is_correct,
            type=MediaType.VIDEO
        )
