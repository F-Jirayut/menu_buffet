from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, datetime, ForeignKey, Text
from app.database import Base
from sqlalchemy.orm import relationship

class OrderPaymentProof(Base):
    __tablename__ = 'order_payment_proofs'

    id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    image_disk = Column(String(50), nullable=False)
    image_path = Column(Text, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    order = relationship("Order", back_populates="payment_proofs")