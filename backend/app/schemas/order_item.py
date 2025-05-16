from operator import ge
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from decimal import Decimal
from datetime import datetime

class OrderItemBase(BaseModel):
    order_id: int
    menu_id: int
    menu_name: str
    quantity: int = Field(default=1, ge=1, le=5)
    price: Decimal = Field(default=0, ge=0)
    status: Literal['pending', 'preparing', 'served', 'cancelled'] = 'pending'
    note: Optional[str] = None
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')},
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[int]
    status: Optional[Literal['pending', 'preparing', 'served', 'cancelled']]
    note: Optional[str] = None

class OrderItemResponse(OrderItemBase):
    id: int

class OrderItemInDB(OrderItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
