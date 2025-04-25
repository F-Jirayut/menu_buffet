from sqlalchemy import Column, BigInteger, String, DateTime, Integer
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class MenuCategory(Base):
    __tablename__ = "menu_categories"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    menus = relationship("Menu", back_populates="menu_category")
