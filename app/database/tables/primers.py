from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.tables.tasks import DbTask


class DbPrimer(DbTask):
    __tablename__ = "primers"

    # FOREIGN KEYS
    # ------------------------------------------------------------------------
    id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True
    )
    bucket_id: Mapped[UUID] = mapped_column(
        ForeignKey("buckets.id"),
        nullable=True
    )
    text_id: Mapped[UUID] = mapped_column(
        ForeignKey("texts.id"),
        nullable=True
    )

    # RELATIONSHIPS
    # ------------------------------------------------------------------------
    bucket: Mapped["DbBucket"] = relationship(
        back_populates="primers"
    )
    text: Mapped["DbText"] = relationship(
        back_populates="primers"
    )

    # CONSTRAINTS
    # ------------------------------------------------------------------------
    __table_args__ = (
        CheckConstraint(
            "text_id IS NOT NULL AND bucket_id IS NULL"
            " OR "
            "text_id IS NULL AND bucket_id IS NOT NULL",
            name="check_primer_text_or_bucket"
        ),
    )

    # CONFIGURATION
    # ------------------------------------------------------------------------
    __mapper_args__ = {
        "polymorphic_identity": "primer"
    }
