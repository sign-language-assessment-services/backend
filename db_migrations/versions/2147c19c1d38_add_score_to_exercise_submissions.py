"""Add score to exercise_submissions

Revision ID: 2147c19c1d38
Revises: 4e0706c45957
Create Date: 2025-04-06 08:31:56.551800+00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# Revision identifiers used by Alembic
revision: str = "2147c19c1d38"
down_revision: Union[str, None] = "4e0706c45957"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "exercise_submissions",
        sa.Column(
            "score",
            sa.Float(),
            nullable=True
        )
    )


def downgrade() -> None:
    op.drop_column("exercise_submissions", "score")
