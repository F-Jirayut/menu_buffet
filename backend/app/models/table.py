from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger, Text, DateTime, ForeignKey, TIMESTAMP
from app.database import Base
from sqlalchemy.orm import relationship

class Table(Base):
    __tablename__ = 'tables'

    id = Column(BigInteger, primary_key=True)
    number = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)
    
    