"""add tables customers, orders and order_payment_proofs

Revision ID: c3cd2fd89e68
Revises: 158a1a3f2581
Create Date: 2025-04-29 16:52:43.932118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3cd2fd89e68'
down_revision: Union[str, None] = '158a1a3f2581'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # customers table
    op.create_table(
        'customers',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('email_sent', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
    )

    # orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('table_id', sa.BigInteger, nullable=False),
        sa.Column('customer_id', sa.BigInteger, nullable=True),
        sa.Column('reserved_at', sa.DateTime(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('ended_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Enum('padding', 'reserved', 'active', 'completed', 'cancelled', name='order_status'), nullable=False),
        sa.Column('deposit_amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('total_price', sa.Numeric(10, 2), nullable=True),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),

        sa.ForeignKeyConstraint(['table_id'], ['tables.id']),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'])
    )

    # order_payment_proofs table
    op.create_table(
        'order_payment_proofs',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('order_id', sa.BigInteger, nullable=False),
        sa.Column('image_disk', sa.String(length=50), nullable=False),
        sa.Column('image_path', sa.Text(), nullable=False),
        sa.Column('is_verified', sa.Boolean, nullable=False, server_default=sa.text('false')),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),

        sa.ForeignKeyConstraint(['order_id'], ['orders.id'])
    )
    pass


def downgrade():
    op.drop_table('order_payment_proofs')
    op.drop_table('orders')
    op.drop_table('customers')
    op.execute("DROP TYPE IF EXISTS order_status")
    pass
