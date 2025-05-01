"""Create menus table

Revision ID: 4c8280234983
Revises: cf33ccc0d903
Create Date: 2025-04-22 18:04:00.129609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c8280234983'
down_revision: Union[str, None] = 'cf33ccc0d903'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'menus',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('image_disk', sa.String(length=50), nullable=True),
        sa.Column('image_path', sa.Text(), nullable=True),
        sa.Column('category_id', sa.BigInteger, sa.ForeignKey('menu_categories.id'), nullable=False),
        sa.Column('is_available', sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
        sa.UniqueConstraint('name')
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('menus')
    pass
