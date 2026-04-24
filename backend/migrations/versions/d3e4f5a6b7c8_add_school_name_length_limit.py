"""add school_name length limit

Revision ID: d3e4f5a6b7c8
Revises: c2d3e4f5a6b7
Create Date: 2026-04-25 01:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'd3e4f5a6b7c8'
down_revision: Union[str, Sequence[str], None] = 'c2d3e4f5a6b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # school_name 컬럼 길이 제한 추가 (String → String(100))
    op.alter_column(
        'exam_analysis',
        'school_name',
        existing_type=sa.String(),
        type_=sa.String(100),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        'exam_analysis',
        'school_name',
        existing_type=sa.String(100),
        type_=sa.String(),
        existing_nullable=False,
    )