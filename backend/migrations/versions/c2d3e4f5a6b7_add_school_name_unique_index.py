"""add school_name unique index

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-04-25 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'c2d3e4f5a6b7'
down_revision: Union[str, Sequence[str], None] = 'b1c2d3e4f5a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # school_name 유니크 제약 추가
    op.create_unique_constraint(
        "uq_exam_analysis_school_name",
        "exam_analysis",
        ["school_name"],
    )
    # school_name 인덱스 추가
    op.create_index(
        "ix_exam_analysis_school_name",
        "exam_analysis",
        ["school_name"],
    )


def downgrade() -> None:
    op.drop_index("ix_exam_analysis_school_name", table_name="exam_analysis")
    op.drop_constraint("uq_exam_analysis_school_name", "exam_analysis", type_="unique")