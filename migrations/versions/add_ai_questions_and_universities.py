"""Initial migration

Revision ID: add_ai_questions_universities
Revises:
Create Date: 2025-01-01 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'add_ai_questions_universities'
down_revision: Union[str, None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('tg_id', sa.BigInteger(), nullable=False),
        sa.Column('points', sa.Integer(), nullable=True),
        sa.Column('ai_questions_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('tg_id')
    )

    op.create_table('professions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profession_name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('universities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('university_name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('professions_universities',
        sa.Column('profession_id', sa.Integer(), nullable=False),
        sa.Column('university_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['profession_id'], ['professions.id'], ),
        sa.ForeignKeyConstraint(['university_id'], ['universities.id'], ),
        sa.PrimaryKeyConstraint('profession_id', 'university_id')
    )


def downgrade() -> None:
    op.drop_table('professions_universities')
    op.drop_table('universities')
    op.drop_table('professions')
    op.drop_table('users')
