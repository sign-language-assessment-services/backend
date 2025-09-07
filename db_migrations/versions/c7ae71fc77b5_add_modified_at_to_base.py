"""Add modified_at to base

Revision ID: c7ae71fc77b5
Revises: 27d43ce7e30e
Create Date: 2025-06-01 17:40:41.730927+00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# Revision identifiers used by Alembic
revision: str = "c7ae71fc77b5"
down_revision: Union[str, None] = "27d43ce7e30e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "assessment_submissions",
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        )
    )
    op.add_column(
        "assessments",
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        )
    )
    op.add_column(
        "assessments_tasks",
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        )
    )
    op.add_column(
        "bucket_objects",
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        )
    )
    op.add_column(
        "choices",
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        )
    )
    op.add_column(
        "exercise_submissions",
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        )
    )
    op.add_column(
        "multiple_choices",
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        )
    )
    op.add_column(
        "multiple_choices_choices",
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        )
    )
    op.add_column(
        "tasks",
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        )
    )


def downgrade() -> None:
    op.drop_column(
        "tasks",
        "modified_at"
    )
    op.drop_column(
        "multiple_choices_choices",
        "modified_at"
    )
    op.drop_column(
        "multiple_choices",
        "modified_at"
    )
    op.drop_column(
        "exercise_submissions",
        "modified_at"
    )
    op.drop_column(
        "choices",
        "modified_at"
    )
    op.drop_column(
        "bucket_objects",
        "modified_at"
    )
    op.drop_column(
        "assessments_tasks",
        "modified_at"
    )
    op.drop_column(
        "assessments",
        "modified_at"
    )
    op.drop_column(
        "assessment_submissions",
        "modified_at"
    )
