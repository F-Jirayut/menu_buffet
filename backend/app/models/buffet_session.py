from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger, Text, DateTime, ForeignKey, Boolean, TIMESTAMP
from app.database import Base
from sqlalchemy.orm import relationship

class BuffetSession(Base):
    __tablename__ = 'buffet_sessions'

    id = Column(BigInteger, primary_key=True)
    qr_code = Column(String(255), unique=True, nullable=False)
    is_used = Column(Boolean, nullable=False, server_default='false')
    started_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    table_id = Column(BigInteger, ForeignKey('tables.id'), nullable=False)
    admin_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())