from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.tasks import DbTask


class DbExercise(DbTask):
    __tablename__ = "exercises"

    # COLUMNS
    # ------------------------------------------------------------------------
    points: Mapped[int] = mapped_column(
        nullable=False,
        default="1"
    )

    # FOREIGN_KEYS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )
    bucket_object_id: Mapped[UUID] = mapped_column(
        ForeignKey("bucket_objects.id"),
        nullable=False
    )
    multiple_choice_id: Mapped[UUID] = mapped_column(
        ForeignKey("multiple_choices.id")
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    bucket_object: Mapped["DbBucketObjects"] = relationship(
        back_populates="exercises"
    )
    multiple_choice: Mapped["DbMultipleChoice"] = relationship(
        back_populates="exercises"
    )
    submissions: Mapped[list["DbSubmission"]] = relationship(
        back_populates="exercise"
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_identity": "exercise"
    }
