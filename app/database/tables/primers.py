from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.tasks import DbTask
from app.database.type_hints import Bucket, Text


class DbPrimer(DbTask):
    __tablename__ = "primers"

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True
    )
    text_id: Mapped[UUID] = mapped_column(
        ForeignKey("texts.id")
    )
    bucket_id: Mapped[UUID] = mapped_column(
        ForeignKey("buckets.id")
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    text: Mapped[Text] = relationship(
        back_populates="primers"
    )
    bucket: Mapped[Bucket] = relationship(
        back_populates="primers"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    CheckConstraint(
        "text_id IS NOT NULL AND bucket_id IS NULL"
        " OR "
        "text_id IS NULL AND bucket_id IS NOT NULL",
        name="check_primer_text_or_bucket"
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_identity": "primer"
    }
