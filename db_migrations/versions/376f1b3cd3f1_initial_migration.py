"""Initial migration

Revision ID: 376f1b3cd3f1
Revises: 
Create Date: 2024-10-27 09:13:53.548810+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "376f1b3cd3f1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("assessments",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.Column(
            "name",
            sa.Unicode(length=100),
            nullable=False
        ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table("buckets",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.Column(
            "bucket",
            sa.String(length=63),
            nullable=False
        ),
        sa.Column(
            "key",
            sa.Unicode(length=1024),
            nullable=False
        ),
        sa.Column(
            "mediatype",
            sa.Enum(
                "IMAGE",
                "VIDEO",
                name="mediatype"
            ),
            nullable=False
        ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table("multiple_choice",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False),
        sa.Column(
            "random",
            sa.Boolean(),
            nullable=False
        ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "tasks",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.Column(
            "task_type",
            sa.String(length=8),
            nullable=False
        ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "texts",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.Column(
            "text",
            sa.UnicodeText(),
            nullable=False
        ),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "choices",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.Column(
            "is_correct",
            sa.Boolean(),
            nullable=False
        ),
        sa.Column(
            "position",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "multiple_choice_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "text_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(["multiple_choice_id"], ["multiple_choice.id"]),
        sa.ForeignKeyConstraint(["text_id"], ["texts.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "exercises",
        sa.Column(
            "id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "text_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "bucket_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "multiple_choice_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(["bucket_id"], ["buckets.id"]),
        sa.ForeignKeyConstraint(["id"], ["tasks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["multiple_choice_id"], ["multiple_choice.id"]),
        sa.ForeignKeyConstraint(["text_id"], ["texts.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "primers",
        sa.Column(
            "id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "text_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "bucket_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(["bucket_id"], ["buckets.id"]),
        sa.ForeignKeyConstraint(["id"], ["tasks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["text_id"], ["texts.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "submissions",
        sa.Column(
            "id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.Column(
            "user_name",
            sa.String(length=36),
            nullable=False
        ),
        sa.Column(
            "exercise_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "submission_type",
            sa.String(length=26),
            nullable=False
        ),
        sa.ForeignKeyConstraint(["exercise_id"], ["exercises.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "multiple_choice_submissions",
        sa.Column(
            "id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "multiple_choice_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(["id"], ["submissions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["multiple_choice_id"], ["multiple_choice.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "text_submissions",
        sa.Column(
            "id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "text",
            sa.Text(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(["id"], ["submissions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:
    op.drop_table("text_submissions")
    op.drop_table("multiple_choice_submissions")
    op.drop_table("submissions")
    op.drop_table("primers")
    op.drop_table("exercises")
    op.drop_table("choices")
    op.drop_table("texts")
    op.drop_table("tasks")
    op.drop_table("multiple_choice")
    op.drop_table("buckets")
    op.drop_table("assessments")
