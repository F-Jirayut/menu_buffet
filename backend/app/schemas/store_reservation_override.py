from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional

class StoreReservationOverrideBase(BaseModel):
    id: int
    date: date
    open_time: Optional[time]
    close_time: Optional[time]
    is_closed: bool
    note: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class StoreReservationOverrideCreate(BaseModel):
    date: date
    open_time: Optional[time]
    close_time: Optional[time]
    is_closed: bool = False
    note: Optional[str] = None

class StoreReservationOverrideUpdate(BaseModel):
    open_time: Optional[time]
    close_time: Optional[time]
    is_closed: Optional[bool]
    note: Optional[str]
