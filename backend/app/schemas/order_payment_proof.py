from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderPaymentProofBase(BaseModel):
    order_id: int
    image_disk: str
    image_path: str
    is_verified: Optional[bool] = False
    note: Optional[str] = None


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
