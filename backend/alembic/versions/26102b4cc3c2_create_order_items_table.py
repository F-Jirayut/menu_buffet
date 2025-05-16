"""create order_items table

Revision ID: 26102b4cc3c2
Revises: 4567ed96aa57
Create Date: 2025-05-15 16:39:06.582516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26102b4cc3c2'
down_revision: Union[str, None] = '4567ed96aa57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'order_items',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('order_id', sa.BigInteger, sa.ForeignKey('orders.id'), nullable=False),
        sa.Column('menu_id', sa.BigInteger, sa.ForeignKey('menus.id'), nullable=False),
        sa.Column('menu_name', sa.String(length=255), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False, default=1),
        sa.Column('price', sa.Numeric(10, 2), nullable=False, default=0),
        sa.Column('status', sa.Enum('pending', 'preparing', 'served', 'cancelled', name='order_item_status'), nullable=False, server_default='pending'),
        sa.Column('note', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

def downgrade():
    op.drop_table('order_items')
    op.execute("DROP TYPE IF EXISTS order_item_status")