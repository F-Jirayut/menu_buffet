"""add new tables

Revision ID: 158a1a3f2581
Revises: 2302ffc5d3a5
Create Date: 2025-04-29 13:04:35.420512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = '158a1a3f2581'
down_revision: Union[str, None] = '2302ffc5d3a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'tables',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tables')
    pass
