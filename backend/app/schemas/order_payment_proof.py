from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class OrderPaymentProofBase(BaseModel):
    order_id: int
    image_disk: str
    image_path: str
    is_verified: Optional[bool] = False
    note: Optional[str] = None
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )


class OrderPaymentProofCreate(OrderPaymentProofBase):
    pass


class OrderPaymentProofUpdate(BaseModel):
    is_verified: Optional[bool] = None
    note: Optional[str] = None


class OrderPaymentProofInDB(OrderPaymentProofBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
