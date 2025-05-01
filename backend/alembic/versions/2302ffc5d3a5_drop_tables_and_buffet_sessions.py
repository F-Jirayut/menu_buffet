"""drop tables and buffet_sessions

Revision ID: 2302ffc5d3a5
Revises: 85465642ca19
Create Date: 2025-04-29 13:03:35.844303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2302ffc5d3a5'
down_revision: Union[str, None] = '85465642ca19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: drop tables and buffet_sessions."""
    # Drop 'tables' table
    op.drop_table('tables')
    pass


def downgrade() -> None:
    """Downgrade schema: recreate tables and buffet_sessions."""
    # Recreate 'tables' table
    op.create_table(
        'tables',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('number', sa.String(length=255), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    pass
