from sqlalchemy import (
    Column, BigInteger, SmallInteger, Time, Boolean,TIMESTAMP, func
)
from app.database import Base

class StoreReservationSetting(Base):
    __tablename__ = 'store_reservation_settings'

    id = Column(BigInteger, primary_key=True)
    day_of_week = Column(SmallInteger, nullable=False)  # 0 = Sunday, 6 = Saturday
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default='true')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
