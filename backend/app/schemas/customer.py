from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    email_sent: Optional[bool] = None


class CustomerInDB(CustomerBase):
    id: int
    email_sent: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
