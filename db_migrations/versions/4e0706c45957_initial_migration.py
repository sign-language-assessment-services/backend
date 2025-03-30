"""Initial migration

Revision ID: 4e0706c45957
Revises: 
Create Date: 2025-03-24 16:28:50.879748+00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4e0706c45957"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assessments",

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
        sa.Column(
            "deadline",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        ),
        sa.Column(
            "max_attempts",
            sa.Integer(),
            nullable=True
        ),

        sa.PrimaryKeyConstraint("id")
    )
    
    op.create_table(
        "bucket_objects",

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
            "media_type",
            sa.Enum("IMAGE", "VIDEO", name="mediatype"),
            nullable=False
        ),

        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("bucket", "key")
    )

    op.create_table(
        "multiple_choices",

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
        "assessment_submissions",

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
            "user_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "score",
            sa.Float(),
            nullable=True
        ),
        sa.Column(
            "finished_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True
        ),
        sa.Column(
            "assessment_id",
            sa.Uuid(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"]),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_table(
        "assessments_tasks",

        sa.Column(
            "position",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "assessment_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "task_id",
            sa.Uuid(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(["assessment_id"], ["assessments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("assessment_id", "task_id"),
        sa.UniqueConstraint("assessment_id", "position")
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
            "bucket_object_id",
            sa.Uuid(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(["bucket_object_id"], ["bucket_objects.id"]),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_table(
        "exercises",

        sa.Column(
            "points",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "bucket_object_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "multiple_choice_id",
            sa.Uuid(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(["bucket_object_id"], ["bucket_objects.id"]),
        sa.ForeignKeyConstraint(["id"], ["tasks.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["multiple_choice_id"], ["multiple_choices.id"]),
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
            "bucket_object_id",
            sa.Uuid(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(["bucket_object_id"], ["bucket_objects.id"]),
        sa.ForeignKeyConstraint(["id"], ["tasks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_table(
        "exercise_submissions",

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
            "user_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "choices",
            postgresql.ARRAY(sa.Uuid(), dimensions=1),
            nullable=True
        ),
        sa.Column(
            "assessment_submission_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "exercise_id",
            sa.Uuid(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(["assessment_submission_id"], ["assessment_submissions.id"]),
        sa.ForeignKeyConstraint(["exercise_id"], ["exercises.id"]),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_table(
        "multiple_choices_choices",

        sa.Column(
            "position",
            sa.Integer(),
            nullable=False
        ),
        sa.Column(
            "is_correct",
            sa.Boolean(),
            nullable=False
        ),
        sa.Column(
            "choice_id",
            sa.Uuid(),
            nullable=False
        ),
        sa.Column(
            "multiple_choice_id",
            sa.Uuid(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(["choice_id"], ["choices.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["multiple_choice_id"], ["multiple_choices.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("choice_id", "multiple_choice_id"),
        sa.UniqueConstraint("multiple_choice_id", "position")
    )


def downgrade() -> None:
    op.drop_table("multiple_choices_choices")
    op.drop_table("exercise_submissions")
    op.drop_table("primers")
    op.drop_table("exercises")
    op.drop_table("choices")
    op.drop_table("assessments_tasks")
    op.drop_table("assessment_submissions")
    op.drop_table("tasks")
    op.drop_table("multiple_choices")
    op.drop_table("bucket_objects")
    op.drop_table("assessments")

    op.execute("DROP TYPE mediatype")
