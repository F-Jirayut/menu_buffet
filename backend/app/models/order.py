from sqlalchemy import Column, BigInteger, String, DateTime, Integer, Boolean, ForeignKey, Enum, Numeric, Text
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, primary_key=True)
    table_id = Column(BigInteger, ForeignKey('tables.id'), nullable=False)
    customer_id = Column(BigInteger, ForeignKey('customers.id'), nullable=True)
    reserved_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=False)
    status = Column(Enum('pending', 'reserved', 'active', 'completed', 'cancelled', name='order_status'), nullable=False)
    deposit_amount = Column(Numeric(10, 2), nullable=True)
    total_price = Column(Numeric(10, 2), nullable=True)
    note = Column(Text, nullable=True)
    email_sent = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    payment_proofs = relationship("OrderPaymentProof", back_populates="order")