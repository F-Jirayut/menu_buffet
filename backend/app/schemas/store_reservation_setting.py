from datetime import time, datetime
from pydantic import BaseModel, conint
from typing import Optional

# สำหรับการอ่านข้อมูล (เช่น response)
class StoreReservationSettingBase(BaseModel):
    id: int
    day_of_week: conint(ge=0, le=6)  # 0 = Sunday, 6 = Saturday
    open_time: Optional[time]
    close_time: Optional[time]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# สำหรับการสร้างข้อมูลใหม่ (เช่น POST)
class StoreReservationSettingCreate(BaseModel):
    day_of_week: conint(ge=0, le=6)
    open_time: Optional[time]
    close_time: Optional[time]
    is_active: bool = True


# สำหรับการอัปเดตข้อมูล (PATCH/PUT)
class StoreReservationSettingUpdate(BaseModel):
    open_time: Optional[time]
    close_time: Optional[time]
    is_active: Optional[bool]
