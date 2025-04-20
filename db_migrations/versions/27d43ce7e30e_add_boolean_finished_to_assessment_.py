"""Add boolean finished to assessment_submissions

Revision ID: 27d43ce7e30e
Revises: 2147c19c1d38
Create Date: 2025-04-20 08:22:18.799175+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "27d43ce7e30e"
down_revision: Union[str, None] = "2147c19c1d38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "assessment_submissions",
        sa.Column(
            "finished",
            sa.Boolean(),
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column(
        "assessment_submissions",
        "finished"
    )
