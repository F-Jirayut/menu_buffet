"""drop deposit_amount from orders

Revision ID: 4567ed96aa57
Revises: 58d37eab5716
Create Date: 2025-05-15 09:22:49.670548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4567ed96aa57'
down_revision: Union[str, None] = '58d37eab5716'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('orders', 'deposit_amount')

def downgrade():
    op.add_column('orders', sa.Column('deposit_amount', sa.Numeric(10, 2), nullable=True))
