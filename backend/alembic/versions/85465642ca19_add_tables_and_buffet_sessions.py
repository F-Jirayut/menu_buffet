"""add tables and buffet_sessions

Revision ID: 85465642ca19
Revises: 4c8280234983
Create Date: 2025-04-27 18:42:58.415472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85465642ca19'
down_revision: Union[str, None] = '4c8280234983'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create "tables"
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


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tables')
    pass
