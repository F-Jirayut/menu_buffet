from app.schemas.customer import CustomerBase
from pydantic import BaseModel, root_validator, validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal


class OrderBase(BaseModel):
    table_id: int
    reserved_at: Optional[datetime] = None
    started_at: datetime
    ended_at: datetime
    status: Literal['pending', 'reserved', 'active', 'completed', 'cancelled']
    deposit_amount: Optional[Decimal] = None
    total_price: Optional[Decimal] = None
    note: Optional[str] = None
    email_sent: Optional[bool] = None
    
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')},
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )


class OrderCreate(OrderBase):
    customer_id: Optional[int] = None
    @root_validator(pre=True)
    
    def check_dates(cls, values):
        started_at = values.get('started_at')
        ended_at = values.get('ended_at')

        if started_at and ended_at and started_at >= ended_at:
            raise ValueError("'started_at' must be before 'ended_at'")
        return values
    
    pass


class OrderUpdate(OrderBase):
    customer_id: Optional[int] = None

class OrderResponse(OrderBase):
    id: int
    customer: Optional[CustomerBase] = None

class OrderInDB(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
