from sqlalchemy import Column, BigInteger, String, Integer, Numeric, Enum, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(BigInteger, primary_key=True, index=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    menu_id = Column(BigInteger, ForeignKey('menus.id'), nullable=False)
    menu_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False, default=0)
    status = Column(Enum('pending', 'preparing', 'served', 'cancelled', name='order_item_status'), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship("Order", back_populates="order_items")
    menu = relationship("Menu", back_populates="order_items")
