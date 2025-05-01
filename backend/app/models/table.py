from sqlalchemy import Column, BigInteger, String, Integer, Text, Boolean, TIMESTAMP, func
from app.database import Base

class Table(Base):
    __tablename__ = 'tables'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    note = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default='true')
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)
