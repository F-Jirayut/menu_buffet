from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from decimal import Decimal


class OrderBase(BaseModel):
    table_id: int
    customer_id: Optional[int] = None
    reserved_at: Optional[datetime] = None
    started_at: datetime
    ended_at: datetime
    status: Literal['padding', 'reserved', 'active', 'completed', 'cancelled']
    deposit_amount: Optional[Decimal] = None
    total_price: Optional[Decimal] = None
    note: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderInDB(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
