from app.schemas.customer import CustomerResponse
from app.schemas.order_item import OrderItemInDB
from pydantic import BaseModel, model_validator, validator, ConfigDict
from typing import Optional, Literal, List
from datetime import datetime
from decimal import Decimal

class OrderBase(BaseModel):
    table_id: int
    reserved_at: Optional[datetime] = None
    started_at: datetime
    ended_at: datetime
    status: Literal['pending', 'reserved', 'active', 'completed', 'cancelled']
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
    
    @model_validator(mode="before")
    def check_dates(cls, values):
        started_at = values.get('started_at')
        ended_at = values.get('ended_at')

        if started_at and ended_at and started_at >= ended_at:
            raise ValueError("'started_at' must be before 'ended_at'")
        return values


class OrderUpdate(OrderBase):
    customer_id: Optional[int] = None
    
    @model_validator(mode="before")
    def check_dates(cls, values):
        started_at = values.get('started_at')
        ended_at = values.get('ended_at')
        if started_at and ended_at and started_at >= ended_at:
            raise ValueError("'started_at' must be before 'ended_at'")
        return values

class OrderItemGroup(BaseModel):
    created_at: datetime
    order_items: List[OrderItemInDB]
    
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')})

class OrderResponse(OrderBase):
    id: int
    customer: Optional[CustomerResponse] = None
    order_items: Optional[List[OrderItemInDB]] = None
    group_order_items: Optional[List[OrderItemGroup]] = None

class OrderInDB(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
