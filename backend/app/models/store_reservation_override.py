from sqlalchemy import (
    Column, BigInteger, Time, Boolean,
    Date, Text, TIMESTAMP, func
)
from app.database import Base

class StoreReservationOverride(Base):
    __tablename__ = 'store_reservation_overrides'

    id = Column(BigInteger, primary_key=True)
    date = Column(Date, nullable=False)
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    is_closed = Column(Boolean, nullable=False, server_default='false')
    note = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())