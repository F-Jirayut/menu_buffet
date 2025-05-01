"""Add store_reservation_settings and store_reservation_overrides tables

Revision ID: 58d37eab5716
Revises: c3cd2fd89e68
Create Date: 2025-04-29 17:25:47.977778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58d37eab5716'
down_revision: Union[str, None] = 'c3cd2fd89e68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'store_reservation_settings',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('day_of_week', sa.SmallInteger, nullable=False),
        sa.Column('open_time', sa.Time(), nullable=True),
        sa.Column('close_time', sa.Time(), nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.UniqueConstraint('day_of_week')
    )
    

    # Create store_reservation_overrides table
    op.create_table(
        'store_reservation_overrides',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('open_time', sa.Time(), nullable=True),
        sa.Column('close_time', sa.Time(), nullable=True),
        sa.Column('is_closed', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.UniqueConstraint('date')
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('store_reservation_settings')
    op.drop_table('store_reservation_overrides')
    pass
