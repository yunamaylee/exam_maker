"""add fk and json column to exam_result

Revision ID: b1c2d3e4f5a6
Revises: 8af4be0a8355
Create Date: 2026-04-24 22:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'b1c2d3e4f5a6'
down_revision: Union[str, Sequence[str], None] = '8af4be0a8355'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'exam_result',
        'exam_content',
        existing_type=sa.Text(),
        type_=sa.JSON(),
        existing_nullable=False,
        postgresql_using='exam_content::json',
    )
    op.create_foreign_key(
        'fk_exam_result_analysis_id',
        'exam_result',
        'exam_analysis',
        ['analysis_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.alter_column(
        'exam_analysis',
        'created_at',
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
    )
    op.alter_column(
        'exam_result',
        'created_at',
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.drop_constraint(
        'fk_exam_result_analysis_id',
        'exam_result',
        type_='foreignkey',
    )
    op.alter_column(
        'exam_result',
        'exam_content',
        existing_type=sa.JSON(),
        type_=sa.Text(),
        existing_nullable=False,
        postgresql_using='exam_content::text',
    )
    op.alter_column(
        'exam_analysis',
        'created_at',
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
    op.alter_column(
        'exam_result',
        'created_at',
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
